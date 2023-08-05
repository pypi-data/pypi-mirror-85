import click
import os
import sys
import json
import docker
from pprint import pprint
from textwrap import dedent
from scora.models.blocks import BlocksConfig
from scora.helpers.misc import getdir
from scora.helpers.terminal import title, prompt
from scora.helpers.aws import confirm_identity, session
from scora.helpers.aws import get_cfn_substack_id, get_cfn_resource_prop
from scora.helpers.aws import create_airflow_access_point
from scora.helpers.aws import ecs_get_latest_taskrev, get_ecs_volume
from scora.helpers.aws import ecs_get_latest_task_definition
from scora.helpers.aws import get_ecs_taskdef_register_params


def get_yaml(dir=None, new=True, show_prompt=True):
    """Gets the yaml file optionally asking to confirm. The prompt
    can either ask if the user wants to write a new file or ask to use the
    given file

    Args:
        dir (str, optional): The directory where to read the blocks.yaml from.
        new (bool, optional): When prompt is true, message should prompt \
            for new file. Defaults to True.
        show_prompt (bool, optional): Show prompt or not, when no prompt, the\
            function only returns the tuple (env_file, dir). Defaults to True.

    Returns:
        env_file and dir (tuple): (env_file, dir)
    """
    dir = getdir(dir)
    title('📁 Working directory')
    click.secho(f'Working dir : {dir}')
    env_file = f'{dir}/blocks.yaml'

    # TODO : check if the file exists
    if show_prompt:
        if new:
            msg = f"""
                We're going to start to build a new file {env_file},
                Would you like to continue? """
        else:

            msg = f"""
                Going to use the file  {env_file},
                Would you like to continue?"""

        prompt(dedent(msg), abort=True, prompt_method=click.confirm)

    return (env_file, dir)


# -----------------------------------------------
#  Core of the blocks specific implementation
# -----------------------------------------------

def init(profile=None, dir=False, templates_bucket="oncase-prj-templates"):
    """ - Shows the user identity and ask for confirmation;
    - Shows the working dir/file and confirms;
    - Starts building the blocks.yaml file;

    Args:
        profile (str, optional): The AWS Profilw to use. Defaults to None.
        dir (str, optional): The optional relative path to resolve. \
          Defaults to None.
        templates_bucket (str, optional): Bucket to temporary hold the \
            Cloudformation templates. Defaults to `oncase-prj-templates`.
    """
    title('🚀 Blocks init')
    confirm_identity(profile)

    env_file, dir = get_yaml(dir, new=True)

    config = BlocksConfig()

    title('📝 Project-specific variables')
    # Project config
    prj_name = prompt("Please type the project friendly name",
                      default="My Project",
                      show_default=True,
                      prompt_method=click.prompt,
                      type=click.types.STRING)  # TODO : validate
    config.project.set_name(prj_name)

    prj_key = prompt("Please type the project unique key",
                     default="my-project",
                     prompt_method=click.prompt,
                     type=click.types.STRING)  # TODO : validate
    config.project.set_key(prj_key)

    prj_region = prompt(
        "Please the region to which you wish to deploy",
        default="us-east-2", prompt_method=click.prompt,
        type=click.types.STRING)  # TODO : validate or multiple choice
    config.project.set_region(prj_region)

    prj_templates_bckt = prompt(
        dedent(
            """
            Please point where should be stored the project templates.\n
            For projects hosted at Oncase, keep the default."""),
        prompt_method=click.prompt, default=templates_bucket,
        type=click.types.STRING)
    config.project.set_templates_bucket(prj_templates_bckt)

    prj_bucket = prompt(
        dedent(
            """
            Please type the project bucket; If you wish to create a new one
            type the desired name and confirm the bucket creation later """),
        prompt_method=click.prompt, default=f"on-{prj_key}",
        type=click.types.STRING)
    config.set_resource_param("bucket", "bucket", prj_bucket)

    # Blocks opt-ins
    title('📦 Resources to provision')

    has_bucket = prompt(
        "\nCreate a new bucket for the project? \n"
        "(if there's an existing one, just answer No)",
        prompt_method=click.confirm)
    config.set_resource_param("bucket", "create", has_bucket)

    config.set_resource_param("domain", "create", True)
    domain = prompt(
        "\n[DNS] What domain will be the parent of this projects parket zone?\n"
        "Defaults to 'onca.se' so that the parked zone is"
        f" {prj_key}.onca.se",
        type=click.types.STRING,
        default="onca.se",
        prompt_method=click.prompt)
    config.set_resource_param("domain", "domain", domain)

    has_athena = prompt(
        "\nCreate an Athena instance mapping the project bucket?",
        prompt_method=click.confirm,
    )
    config.set_resource_param("athena", "create", has_athena)

    has_efs = prompt(
        "\nCreate an EFS Drive?",
        prompt_method=click.confirm,
    )
    config.set_resource_param("efs", "create", has_efs)

    has_rds = prompt(
        "\nCreate a RDS Instance?",
        prompt_method=click.confirm,
    )
    config.set_resource_param("rds", "create", has_rds)

    has_airflow = prompt(
        "\nCreate an Airflow instance?",
        prompt_method=click.confirm,
    )
    config.set_resource_param("airflow", "create", has_airflow)

    has_metabase = prompt(
        "\nCreate a Metabase instance?",
        prompt_method=click.confirm,
    )
    config.set_resource_param("metabase", "create", has_metabase)

    has_identity = prompt(
        "\nCreate Identity pool/provider?",
        prompt_method=click.confirm,
    )
    config.set_resource_param("identity", "create", has_identity)

    has_frontend = prompt(
        "\nCreate Frontend distributions prod/dev?",
        prompt_method=click.confirm,
    )
    config.set_resource_param("frontend", "create", has_frontend)

    has_sandboxing = prompt(
        "\nCreate Sandboxing/Notebooks environment?",
        prompt_method=click.confirm,
    )
    config.set_resource_param("sandboxing", "create", has_sandboxing)

    has_redshift = prompt(
        "\nCreate a Redshift instance?",
        prompt_method=click.confirm,
    )
    config.set_resource_param("redshift", "create", has_redshift)

    has_extension = prompt(
        "\nCreate a Extension entry point?",
        prompt_method=click.confirm,
    )
    config.set_resource_param("extension", "create", has_extension)

    config.set_resource_param("airflow", "start", False)
    config.set_resource_param("airflow", "taskrev", -1)
    config.set_resource_param("metabase", "start", False)

    if has_rds:
        rds_instance_type = prompt(
            "\n[RDS] Please RDS Instance Type you wish to deploy",
            prompt_method=click.prompt,
            type=click.types.STRING,
            default="db.t2.micro")
        config.set_resource_param("rds", "instance_type", rds_instance_type)

    if has_sandboxing:
        prj_repo = prompt(
            "\n[Sandboxing] Please type the repository where you're"
            "going to save the Noteboooks",
            prompt_method=click.prompt,
            type=click.types.STRING)
        config.set_resource_param("sandboxing", "repo", prj_repo)

        notebooks_branch = prompt(
            "\n[Sandboxing] Please type the repository branch where you're "
            "going to save the Noteboooks",
            prompt_method=click.prompt,
            type=click.types.STRING)
        config.set_resource_param("sandboxing", "branch", notebooks_branch)

    config.serialize_to_file(env_file)
    title('❓ Time to push')
    should_push = prompt(
        "\nYour configuration file has been prepared "
        "and it's ready to be used and versioned. \n"
        "Would you like to publish your stack now? ",
        prompt_method=click.confirm
    )
    if should_push:
        push(dir=dir, profile=profile,
             identity_confirmed=True, dir_confirmed=True)


def delete(profile=None, dir=None):
    """ Attemps to delete (on Cloudformation) the stack referenced within
    the blocks.yaml file

    Args:
        profile (str, optional): The AWS Profilw to use. Defaults to None.
        dir (str, optional): The optional relative path to resolve. \
          Defaults to None.
    """
    env_file, dir = get_yaml(dir, show_prompt=False)
    config = BlocksConfig(conf_file=env_file)

    should_delete = prompt(dedent(f"""
        Should delete the stack with the name {config.project.key}
        in {config.project.region}?\n"""), prompt_method=click.confirm,)

    if should_delete:
        click.echo("Deleting...")
        cloudformation = session(
            profile,
            region_name=config.project.region).client('cloudformation')
        cloudformation.delete_stack(StackName=config.project.key)


def push(profile=None, dir=None, identity_confirmed=False,
         dir_confirmed=False):
    """Pushes the contents of the blocks.yaml file to a Cloudformation Stack

    Args:
        profile (str, optional): The AWS Profilw to use. Defaults to None.
        dir (str, optional): The optional relative path to resolve. \
          Defaults to None.
        identity_confirmed (bool, optional): Whether to ask again for identity\
            confirmation.
        dir_confirmed (bool, optional): Whether to ask again for directory\
            confirmation.
    """

    dir = getdir(dir)
    title('🛫 Blocks Push')

    env_file, dir = get_yaml(dir, show_prompt=(not dir_confirmed), new=False)

    config = BlocksConfig(conf_file=env_file)
    vars_values = config.get_stack_vars()

    prompt("Going to use the following params: ", prompt_method=click.secho)
    print(json.dumps(vars_values, indent=4))
    prompt("Would you like to continue?", prompt_method=click.confirm)

    # Additional AWS environment variables

    if not identity_confirmed:
        confirm_identity(profile, region_name=config.project.region)

    # TODO : tried using session keys, but cognito doesn't work with session v
    vars_values["AWS_ACCESS_KEY_ID"] = os.environ.get(
        "AWS_ACCESS_KEY_ID", None)
    vars_values["AWS_SECRET_ACCESS_KEY"] = os.environ.get(
        "AWS_SECRET_ACCESS_KEY", None)

    if not vars_values["AWS_ACCESS_KEY_ID"
                       ] or not vars_values["AWS_SECRET_ACCESS_KEY"]:
        click.secho(dedent("""
            For pushing stacks it's necessary to setup
            AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY
            due to AWS Serverless requirements"""))
        sys.exit()

    vars_values["AWS_DEFAULT_REGION"] = vars_values["PRJREGION"]
    vars_values["AWS_PROFILE"] = "default"

    docker_img = config.docker_img or "oncase/scora-blocks:latest"
    click.echo(f"Pushing blocks using image: {docker_img}")

    client = docker.from_env()
    container = client.containers.run(docker_img, "push",
                                      environment=vars_values,
                                      detach=True, remove=True)

    if not config.docker_img:
        img_id = container.attrs["Image"]
        img = client.images.get(img_id)
        config.docker_img = img.attrs["RepoDigests"][0]
        click.echo(f"Saving the digest of the image used: {config.docker_img}")
        config.serialize_to_file(env_file)

    for lin in container.logs(stream=True):
        print(lin.strip().decode('UTF-8'))


def efs_mount(profile=None, dir=None, identity_confirmed=False,
              dir_confirmed=False):
    """Mounts EFS to the apache airflow TaskDefinition\n
    * Creates the client access on EFS if they don't exist \n
    * Updates the airflow task definition to create mounts for requirements \
        and dags if they aren't configured;\n
    * Updates the local blocks.yaml to be pushed manually

    Args:
        profile (str, optional): The AWS Profilw to use. Defaults to None.
        dir (str, optional): The optional relative path to resolve. \
          Defaults to None.
    """

    dir = getdir(dir)
    env_file, dir = get_yaml(dir, show_prompt=True, new=False)
    config = BlocksConfig(conf_file=env_file)

    title('🛫 Mount EFS to the Airflow Taskdefinition on ECS')
    confirm_identity(profile, region_name=config.project.region)
    prompt("Would you like to continue with these credentials?",
           prompt_method=click.confirm)

    title("💽 Start of mounting process")
    # Checks if the project has Airflow configured at all
    has_airflow = (config.resources["airflow"] and
                   config.resources["airflow"].create and
                   config.resources["airflow"].create.value)

    # If no Airflow config, get out of here
    if not has_airflow:
        click.echo("\n\n")
        click.echo("The current configuration doesn't seem to include Airflow")
        sys.exit()

    sess = session(profile, region_name=config.project.region)

    ##
    # Cloudformation -- Get the EFS Information
    ##

    cloudformation = sess.client('cloudformation')
    efs_stack_id = get_cfn_substack_id(cloudformation, config, "EFSStack")
    efs_fs_id = get_cfn_resource_prop(
        cloudformation, efs_stack_id, "ResourceType",
        "AWS::EFS::FileSystem", "PhysicalResourceId")

    ##
    # EFS -- Verify APs and create if they don't exist
    ##

    efs = sess.client('efs')
    dags_key = 'dags'
    reqs_key = 'requirements'

    # Checks if the efs drive already has the right client accesses

    # List of current access pointss
    access_points = efs.describe_access_points(FileSystemId=efs_fs_id).get(
        "AccessPoints", []
    )

    # Filters for the ones we're interested in
    airflow_access_points = [
        x for x in access_points if
        x["RootDirectory"]["Path"] == f"/{dags_key}" or
        x["RootDirectory"]["Path"] == f"/{reqs_key}"]

    # If the access points for dags and requirements exist
    if len(airflow_access_points) == 2:
        click.echo(dedent(f"EFS `{efs_fs_id}` Already has the access points"))

        # Store their ids
        dags_ap_id = [x for x in airflow_access_points if x["RootDirectory"]
                      ["Path"] == f"/{dags_key}"][0].get("AccessPointId")
        reqs_ap_id = [x for x in airflow_access_points if x["RootDirectory"]
                      ["Path"] == f"/{reqs_key}"][0].get("AccessPointId")

    # If the access points for dags and requirements don't exist
    else:
        click.echo(dedent(f"EFS `{efs_fs_id}` Creating access points"))

        # Creates EFS AP for Dags and store its id
        dags_ap = create_airflow_access_point(efs, efs_fs_id, dags_key)
        dags_ap_id = dags_ap.get("AccessPointId", None)

        # Creates EFS AP for Requirements and store its id
        requirements_ap = create_airflow_access_point(efs, efs_fs_id, reqs_key)
        reqs_ap_id = requirements_ap.get("AccessPointId", None)

    click.echo(f"Dags access point id: `{dags_ap_id}`")
    click.echo(f"Requirements access point id: `{reqs_ap_id}`")
    click.echo("Storing IDs to configuration -- memory")

    config.set_resource_param("efs", "dags_ap_id", dags_ap_id)
    config.set_resource_param("efs", "reqs_ap_id", reqs_ap_id)

    ##
    # CFN, ECS/AIRFLOW -- Get task info and create vols/mounts if none
    ##
    ecs = sess.client('ecs')

    # Gets the airflow taskdef
    af_stack_id = get_cfn_substack_id(cloudformation, config, "AirflowStack")
    af_taskdef = get_cfn_resource_prop(
        cloudformation, af_stack_id, "LogicalResourceId",
        "AirflowTaskDefinition", "PhysicalResourceId")

    # NOTE: The taskrev on Cloudformation is not necessarily the latest
    af_taskdef = af_taskdef.split("/")[1]
    af_task_family, af_task_rev = af_taskdef.split(":")
    click.echo(f"Found task family on CFN: `{af_task_family}`")
    click.echo(f"Found task rev on CFN: `{af_task_rev}`")

    # Gets the latest revision of this taskdef
    last_rev = ecs_get_latest_taskrev(ecs, af_task_family)
    click.echo(f"Actual last active rev of this task family: {last_rev}")

    # Gets the latest taskdef -- the one we're going to work with
    latest_taskdef = ecs_get_latest_task_definition(ecs, af_task_family)

    # Checks the existing mounts for dags and requirements
    vols = latest_taskdef.get("volumes")
    right_vols = [x for x in vols if x["name"] == dags_key or
                  x["name"] == reqs_key]

    # If they're already mounted
    if len(right_vols) == 2:
        click.echo("The volumes already exist. Considering mounted.")

    # If we still don't have our mounts
    else:
        click.echo("The necessary vols don't exist -- will mount.")

        # Gets the current airflow container definition, don't mix with taskdef
        airflow_container_def = latest_taskdef["containerDefinitions"]
        airflow_container_def = next(
            x for x in airflow_container_def if x["name"] == 'airflow')

        # Gets a list of possible other containers
        other_containers = [x for x in latest_taskdef["containerDefinitions"]
                            if x["name"] != "airflow"]

        # Crafts how the mounts should be, considering previously existing ones
        airflow_mounts = [
            *airflow_container_def["mountPoints"],
            {
                "sourceVolume": dags_key,
                "containerPath": "/usr/local/airflow/dags"
            },
            {
                "sourceVolume": reqs_key,
                "containerPath": "/requirements"
            }
        ]

        # Updates the taskdefinition to the new mountpoints
        airflow_container_def["mountPoints"] = airflow_mounts

        # Prepares params to register taskdef using values from the previous
        # Taskdefinition revision; these are all the method kwargs
        params = get_ecs_taskdef_register_params(latest_taskdef)

        # Calls the register
        new_taskdef = ecs.register_task_definition(
            **params,
            family=af_task_family,
            containerDefinitions=[*other_containers, airflow_container_def],
            volumes=[
                *latest_taskdef.get("volumes", []),
                get_ecs_volume(dags_key, efs_fs_id, dags_ap_id),
                get_ecs_volume(reqs_key, efs_fs_id, reqs_ap_id),
            ]
        )

        # Prints success feedback
        new_revision = new_taskdef["taskDefinition"]["taskDefinitionArn"]
        new_revision = new_revision.split(":").pop()
        click.echo("Just created a new revision for the task family "
                   f"{af_task_family} -- {new_revision}")
        click.echo("---------------------------------")
        pprint(new_taskdef)
        click.echo("---------------------------------")

        click.echo("Storing task revision to configuration -- memory")
        config.set_resource_param("airflow", "taskrev", int(new_revision))

        click.echo("Setting StartAirflow to true")
        config.set_resource_param("airflow", "start", True)

    click.echo(f"Dumping configuration to {env_file}")
    click.echo("You can now inspect your blocks.yaml and run:")
    click.secho("$ scora blocks push", bold=True)
    click.echo("To start your Airflow")
    config.serialize_to_file(env_file)
