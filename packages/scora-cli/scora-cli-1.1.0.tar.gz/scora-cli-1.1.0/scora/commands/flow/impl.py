import click
import sys
import json
import os
from pprint import pprint
from scora.helpers.misc import getdir, get_files_recursively
from scora.helpers.terminal import title, prompt
from scora.helpers.aws import confirm_identity, session, get_stack_bucket
from scora.helpers.aws import wait_for_codebuild, stack_exists
from scora.helpers.aws import ecs_get_latest_task_definition
from scora.helpers.aws import get_ecs_taskdef_register_params
from scora.helpers.ecs_constants import fargate_configs, taskdef_template

default_stack = 'scora-plat'


def push_something(dir=None, env='prod', profile=None, project_key=None,
                   stack_name=default_stack, should_prompt=False, push='dags',
                   requirements_file=None):
    """Pushes dags or requirements to the EFS that is mounted to the airflow
    task, given that the stack was created with scora blocks. If requirements
    are pushed, the service is forced a refresh so that a new container
    takes place and installs the fresh requirements.

    Args:
        dir (str, optional): The directory where the dags are. Defaults to None
        env (str, optional): The environment to where to publish. \
            Defaults to 'prod'.
        profile (str, optional): The aws profile to use. Defaults to None.
        project_key (str, optional): The unique dags project key. \
            Must be unique across the projects of that airflow \
            Defaults to None.
        stack_name (str, optional): The stack name where Airflow is deployed. \
            If using oncase cloud, leave it blank, because it defaults to \
            Scora Platform stack \
            Defaults to default_stack.
        should_prompt (bool, optional): Whether to prompt for confirmations \
            or not. Defaults to False.
        push (str): What to push (dags|requirements). Defaults to dags.
        requirements_file (str): The path to an existing requirements file.
    """

    if push == 'dags' and not project_key:
        click.echo("No project key provided")
        sys.exit()

    dir = getdir(dir)
    title(f'🔥 Flow push {push}')
    confirm_identity(profile)
    if should_prompt:
        prompt("Would you like to continue with these credentials?",
               prompt_method=click.confirm)

    # AWS Session init
    sess = session(profile)

    # Gets stack bucket
    cloudformation = sess.client('cloudformation')
    flow_bucket = get_stack_bucket(cloudformation, stack_name)
    click.echo(f"Using the Airflow bucket: `{flow_bucket}`")

    # Sends the dags|reqs to s3
    commit_list = []
    s3 = sess.client('s3')

    if push == 'dags':
        for rel_path, full_path in get_files_recursively(dir, exclude=['pyc']):
            s3_key = f"airflow/{env}/{project_key}/{rel_path}"
            s3_path = f"s3://{flow_bucket}/{s3_key}"
            click.echo(f"{full_path} --> {s3_path}")
            commit_list.append((full_path, s3_key))

    elif push == 'requirements':
        s3_key = f"airflow/{env}/requirements.txt"
        s3_path = f"s3://{flow_bucket}/{s3_key}"
        full_path = os.path.abspath(requirements_file)

        if not os.path.exists(full_path):
            click.echo(f"The file `{full_path}` doesn't exist")
            sys.exit()

        click.echo(f"{full_path} --> {s3_path}")
        commit_list.append((full_path, s3_key))

    if not commit_list or len(commit_list) == 0:
        click.echo("No file found to copy. please check your parameters")
        sys.exit()

    if should_prompt and not prompt(
            "Would you like to continue?", prompt_method=click.confirm):
        sys.exit()

    click.echo("Sending files to S3...")

    for origin, destination in commit_list:
        s3.upload_file(
            Filename=origin,
            Bucket=flow_bucket,
            Key=destination
        )
    click.echo("✅ Files sent to S3")

    # Going to call the Codebuild job to to synchronize EFS
    codebuild = sess.client('codebuild')

    # Map between the param push and job names
    jobs = {"dags": "dags", "requirements": "req"}

    # Env var overrrides in case of pushing dags
    overrides = {"environmentVariablesOverride": [{
        "name": "DAGS_PRJ_KEY",
        "value": project_key,
        "type": "PLAINTEXT"}]} if push == "dags" else {}

    build = codebuild.start_build(
        projectName=f"{stack_name}-af-{jobs[push]}-update",
        **overrides
    )

    build_id = build.get("build", {}).get("id", None)
    click.echo("Sending files to EFS...")

    # Waits untill the job is done
    wait_for_codebuild(
        codebuild, build_id, msg_ok="✅ Files sent to EFS",
        msg_fail="❌ Files not sent to EFS")


def remove_dags(project_key):
    click.echo(f'run: scora flow remove-dags --project-key {project_key}')


def push_requirements(file):
    click.echo(f'run: scora flow push-requirements --file {file}')


def get_task_definition(dir=".", profile=None, stack_name=default_stack,
                        family=None, should_prompt=True):
    """Creates or retrieves a taskdef and outputs to `taskdef-{FAMILY}.json`.\n
    You need to be or have a profile on the region where
    the `stack_name` is deployed.\n
    It looks up on the region for existing task definitions with the
    provided family name. If it exists it will retrieve the latest \
        revision and save locally;\n
    If no task definition exists with the given family name, it will
    "wizard" you through defining some attributes and then save a local
    representation that can be pushed after reviewing:\n
    * Execution role\n
    * Task Role


    Args:
        dir (str, optional): The directory where to save the task \
            definition file. Defaults to ".".
        profile (str, optional): The aws profile to use. Defaults to None.
            Defaults to None.
        stack_name (str, optional): The stack name where Airflow is deployed. \
            If using oncase cloud, leave it blank, because it defaults to \
            Scora Platform stack \
            Defaults to default_stack.
        family (str): The family name for which the task definition should \
            be created or the latest revision retrieved
        should_prompt (bool, optional): Whether to prompt for confirmations \
            or not. Defaults to False.
    """

    if not family:
        click.echo("No family provided")
        sys.exit()

    dir = getdir(dir)
    sess = session(profile)
    title('📋 Flow get task definition')

    stack_verification(sess, profile, stack_name, should_prompt)

    title('👀 Verifting for existing task definitions')
    ecs = sess.client('ecs')
    latest_taskdef = None
    taskdef_file = os.path.join(dir, f"taskdef-{family}.json")

    try:
        latest_taskdef = ecs_get_latest_task_definition(ecs, family)
        click.echo("Retrieved data from an existing taskdefinition")
        params = get_ecs_taskdef_register_params(latest_taskdef)

        new_taskdef = {
            **params,
            "family": family,
            "revision": latest_taskdef["revision"],
            "containerDefinitions": latest_taskdef["containerDefinitions"],
            "volumes": latest_taskdef.get("volumes", [])
        }
        with open(taskdef_file, 'w') as outfile:
            json.dump(new_taskdef, outfile, indent=4)

        sys.exit()

    except Exception:
        click.echo(
            "No task definition found with this name. Going to "
            "create from scratch")
    title('🆕 Creating brand new task definition locally')

    # Warns that the taskdef will be on the same region of the airflow cluster
    title("📍 The Task definition metadata will point to the same region as"
          "the airflow stack")

    # Prompts for vCPU and mem options
    vcpus, mem = choose_fargate_cpu_mem()

    # Asks for the docker image to use
    docker_img = prompt("What docker image you want to run?",
                        prompt_method=click.prompt
                        )

    # Asks for ports that should be exposed
    ports = prompt_for_container_ports()

    with open(taskdef_file, 'w') as outfile:
        taskdef = json.dumps(taskdef_template, indent=4)
        taskdef = taskdef.replace("____FAMILY____", family)
        taskdef = taskdef.replace("____CORES____", str(int(vcpus) * 1024))
        taskdef = taskdef.replace("____MEMORY____", str(int(mem) * 1024))
        taskdef = taskdef.replace("____CONTAINER_IMAGE____", docker_img)
        taskdef = taskdef.replace("\"____CONTAINER_PORTS____\"",
                                  json.dumps(ports))
        taskdef = taskdef.replace("____AIRFLOW_STACK____", stack_name)
        taskdef = taskdef.replace("____AWS_REGION____", stack_name)

        outfile.write(taskdef)

    # Warns that the content must be reviewed before registering
    click.echo("🎉 Your new task definition template was saved locally and "
               "can be pushed after you enter the task and execution Roles")


def register_task_definition(dir=".", profile=None, stack_name=default_stack,
                             family=None, should_prompt=True):
    """Registers a task definition for a given family using a
    local representation. It looks for `taskdef-{FAMILY}.json` and
    registers a new taskdefinition using this file as the template.\n
    The revision number of the newly created task definition will be stored
    locally on the taskdefinition local file.

    Args:
        dir (str, optional): The directory where to read the task \
            definition file from. Defaults to ".".
        profile (str, optional): The aws profile to use. Defaults to None.
            Defaults to None.
        stack_name (str, optional): The stack name where Airflow is deployed. \
            If using oncase cloud, leave it blank, because it defaults to \
            Scora Platform stack \
            Defaults to default_stack.
        family (str): The family name we're going to use to register a new \
            revision
        should_prompt (bool, optional): Whether to prompt for confirmations \
            or not. Defaults to False.
    """
    if not family:
        click.echo("No family provided")
        sys.exit()

    dir = getdir(dir)
    sess = session(profile)
    taskdef = None
    taskdef_file = os.path.join(dir, f"taskdef-{family}.json")

    try:
        with open(taskdef_file) as f:
            taskdef = json.load(f)

    except Exception as e:
        click.echo(f"Error trying to read {taskdef_file}")
        click.echo("---")
        click.echo(e)
        sys.exit()

    title('🚨 Flow push task definition')

    stack_verification(sess, profile, stack_name, should_prompt)

    ecs = sess.client('ecs')

    try:
        ecs_get_latest_task_definition(ecs, family)
        create_over_existing = prompt(
            "There is an existing family with "
            f"the name {family} "
            "would you like to continue?",
            prompt_method=click.confirm,
            default=False)

        if not create_over_existing:
            sys.exit()

    except Exception:
        click.echo(
            "No task definition found with this name. Going to "
            "register the first revision of its family")

    title('🆕 Creating brand new task definition locally')

    # Prepares params to register taskdef
    params = get_ecs_taskdef_register_params(taskdef)

    # Calls the register
    new_taskdef = ecs.register_task_definition(
        **params,
        family=family,
        containerDefinitions=taskdef["containerDefinitions"]
    )

    title('✅ Task definition registered successfully')
    pprint(new_taskdef)

    title('📌 Saving revision locally')

    with open(taskdef_file, 'r') as f:
        new_taskdef_rev = json.load(f)

    new_taskdef_rev["revision"] = new_taskdef["taskDefinition"]["revision"]

    with open(taskdef_file, 'w') as f:
        json.dump(new_taskdef_rev, f, indent=4)


def stack_verification(sess, profile=None, stack_name=default_stack,
                       should_prompt=True):
    """Does the regular job most implementations on this module require;
    Checks for AWS Identity, Checks if there's a stack with the `stack_name`
    on the region and does the regular prompts and error handling;

    Args:
        sess (boto3 Session): The boto3 session used to query services
        profile (str, optional): The aws profile to use. Defaults to None.
            Defaults to None.
        stack_name (str, optional): The stack name where Airflow is deployed. \
            If using oncase cloud, leave it blank, because it defaults to \
            Scora Platform stack \
            Defaults to default_stack.
        should_prompt (bool, optional): Whether to prompt for confirmations \
            or not. Defaults to False.
    """

    confirm_identity(profile)
    if should_prompt:
        prompt("Would you like to continue with these credentials?",
               prompt_method=click.confirm)

    # Gets stack bucket
    cloudformation = sess.client('cloudformation')
    aiarflow_stack_exists = stack_exists(cloudformation, stack_name)

    if not aiarflow_stack_exists:
        # Just to ensure we're going to work on the same region
        # As the airflow cluster
        click.echo(f"The stack {stack_name} doesn't exist on this region.")
        sys.exit()


def choose_fargate_cpu_mem():
    """Prompts for the default possible fargate run configurations in terms of
    memory and vCPUs

    Returns:
        (tuple): (vcpus, mem) The user choice
    """
    click.echo("These are the supported number of vCPUs and the "
               "corresponding number of memory supported on each"
               "vCPU config")

    for vcpus, mem in fargate_configs.items():
        click.echo(f"vCPUs: {vcpus} // RAM (GB): {mem}")

    cpu_opts = list(map(lambda t: t[0], fargate_configs.items()))

    vcpus = prompt(
        "Choose the amount of vCPUs",
        prompt_method=click.prompt,
        default='1',
        type=click.Choice(cpu_opts),
        show_choices=True,
        show_default=True
    )
    click.echo(f"Chosen {vcpus} vCPUs")
    mem_opts = list(map(lambda m: str(m), fargate_configs[vcpus]))
    mem = prompt(
        "For the vCPU config, choose the amount of RAM for the task",
        prompt_method=click.prompt,
        default=mem_opts[0],
        type=click.Choice(mem_opts),
        show_choices=True,
        show_default=True
    )
    click.echo(f"Chosen {mem} GB Ram")
    return (vcpus, mem)


def prompt_for_container_ports():
    """Prompts for mapping ports until the user gives up so it can add "N"
    desired port mappings to a containerDefinition

    Returns:
        (array of dict): The array of ports to be injected into the container \
        configuration
    """
    ports = []
    should_add_port = prompt(
        "Would you like to map container ports now?",
        prompt_method=click.confirm,
        default=False
    )
    while should_add_port:
        port = prompt(
            "Type the port number between 1 and 65535",
            prompt_method=click.prompt,
            default=0,
            type=int,
            show_default=False
        )
        should_add_port = prompt(
            "Would you like to map another port?",
            prompt_method=click.confirm,
            default=False
        )
        ports.append(port)

    output_ports = list(map(lambda p: {
        "containerPort": int(p),
        "hostPort": int(p),
        "protocol": "tcp"
    }, ports))

    return output_ports
