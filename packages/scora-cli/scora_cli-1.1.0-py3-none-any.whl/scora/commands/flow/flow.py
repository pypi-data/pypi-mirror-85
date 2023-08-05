import click
from . import impl

# Flow Module definition


@click.group()
def flow():
    """Handles pipelines manipulation"""
    pass


@flow.command('push-dags')
@click.option('--dir', '-d', type=str,
              default=None, help="Directory where the dags are")
@click.option('--env', '-e', default='prod', type=str,
              help="The environment you're pushing to (env, prod). "
              "Defaults to prod")
@click.option('--profile', '-p', type=str,
              default=None, help="AWS profile to use")
@click.option('--project-key', '-k', type=str,
              default=None, help="Unique project key to which the dags belong")
@click.option('--stack-name', '-s', type=str,
              default=impl.default_stack,
              help="Stack name. Leave this default if hosted at Oncase AWS")
@click.option('--prompt/--no-prompt', default=True, type=bool,
              help="Won't prompt -- to use on integrations")
def push_dags(dir, env, profile, project_key, stack_name, prompt):
    """Pushes dags to the EFS that is mounted to the airflow task, given that
    the stack was created with scora blocks"""
    impl.push_something(dir, env, profile, project_key, stack_name,
                        should_prompt=prompt)


@flow.command('get-task-definition')
@click.option('--dir', '-d', type=str,
              default=None, help="The directory where to save the task "
              "definition file")
@click.option('--profile', '-p', type=str,
              default=None, help="AWS profile to use")
@click.option('--stack-name', '-s', type=str,
              default=impl.default_stack,
              help="The stack name where Airflow is deployed. "
              "If using oncase cloud, leave it blank, because it defaults to "
              "Scora Platform stack")
@click.option('--family', '-f', type=str,
              default=None,
              help="The family name for which the task definition should "
              "be created or the latest revision retrieved")
@click.option('--prompt/--no-prompt', default=True, type=bool,
              help="Won't prompt -- to use on integrations - doesn't work"
              "when creating a new task definition")
def get_task_definition(dir, profile, stack_name, family, prompt):
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
    * Task Role"""
    impl.get_task_definition(dir, profile, stack_name, family,
                             should_prompt=prompt)


@flow.command('register-task-definition')
@click.option('--dir', '-d', type=str,
              default=None, help="The directory where to read the task "
              "definition file from")
@click.option('--profile', '-p', type=str,
              default=None, help="AWS profile to use")
@click.option('--stack-name', '-s', type=str,
              default=impl.default_stack,
              help="The stack name where Airflow is deployed. "
              "If using oncase cloud, leave it blank, because it defaults to "
              "Scora Platform stack. Used to ensure we're creating at the "
              "same region.")
@click.option('--family', '-f', type=str,
              default=None,
              help="The family name we're going to use to register a new "
              "revision")
@click.option('--prompt/--no-prompt', default=True, type=bool,
              help="Won't prompt -- to use on integrations - doesn't work "
              "when creating a new task definition")
def register_task_definition(dir, profile, stack_name, family, prompt):
    """Registers a task definition for a given family using a
    local representation. It looks for `taskdef-{FAMILY}.json` and
    registers a new taskdefinition using this file as the template.\n
    The revision number of the newly created task definition will be stored
    locally on the taskdefinition local file."""
    impl.register_task_definition(dir, profile, stack_name, family,
                                  should_prompt=prompt)


@flow.command('remove-dags')
@click.option('--project-key', '-k',
              default=None, help="Unique project key to which the dags belong")
def remove_dags(project_key):
    """Removes dags from the Airflow service"""
    impl.remove_dags(project_key)


@flow.command('push-requirements')
@click.option('--env', '-e', default='prod', type=str,
              help="The environment you're pushing to (env, prod). "
              "Defaults to prod")
@click.option('--profile', '-p', type=str,
              default=None, help="AWS profile to use")
@click.option('--stack-name', '-s', type=str,
              default=impl.default_stack,
              help="Stack name. Leave this default if hosted at Oncase AWS")
@click.option('--prompt/--no-prompt', default=True, type=bool,
              help="Won't prompt -- to use on integrations")
@click.option('--requirements-file', '-f', default=None, type=str,
              help="THe requirements.txt file you're trying to push")
def push_requirements(env, profile, stack_name, prompt,
                      requirements_file):
    """Pushes a requirements.txt file to the EFS that is mounted to the
    airfloƒw task, given that the stack was created with scora blocks"""
    impl.push_something(
        dir=None, env=env, profile=profile, project_key=None,
        stack_name=stack_name, should_prompt=prompt, push='requirements',
        requirements_file=requirements_file)
