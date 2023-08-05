import boto3
import click
import time
from botocore.exceptions import ClientError
from .terminal import title
import sys


def session(profile=None, region_name=None):
    """Gets a boto3 session given a profile and a region name

    Args:
        profile (str, optional): The AWS Profilw to use. Defaults to None.
        region_name (str, optional): The AWS Region to use. Defaults to None.

    Returns:
        (boto3.Session): A session that can use to create a client from a
        service
    """
    return boto3.Session(
        profile_name=profile, region_name=region_name)


def get_session_keys(profile=None, region_name=None):
    """Returns a session token that can be used to forrward Access key ID
    and Secret to use instead of the users original key pair. In Cloudformation
    Though it can't be used when attempting to handle some IAM operations.

    Args:
        profile (str, optional): The AWS Profilw to use. Defaults to None.
        region_name (str, optional): The AWS Region to use. Defaults to None.

    Returns:
        sessiontoken (dict)

    """
    client = session(profile, region_name=region_name).client('sts')
    return client.get_session_token()


def confirm_identity(profile, region_name=None):
    """Shows the user AWS identity information and asks for a confirmation to
    continue

    Args:
        profile (str, optional): The AWS Profilw to use. Defaults to None.
        region_name (str, optional): The AWS Region to use. Defaults to None.
    """
    title('🆔 Identity')
    click.secho(
        'Before continuing, please validate the identity you want to ',
        fg='green')
    client = session(profile, region_name=region_name).client('sts')
    caller_id = client.get_caller_identity()
    click.secho(f'Using AWS Profile  : {profile or "No profile provided"}')
    click.secho(f'Current User ID    : {caller_id["UserId"]}')
    click.secho(f'Current Account ID : {caller_id["Account"]}')
    click.secho(f'Current Caller ARN : {caller_id["Arn"]}')


def get_cfn_substack_id(cloudformation, config, substack_name):
    """Gets the ID of a substack given a configuration file (from which)
    We'll get the main stack name) and the substack template name.
    Uses describe_stack_resources, filters for the logical ID and gets
    the PhysicalResourceId.

    Args:
        cloudformation (CloudFormation.Client): The cloudformation client
        config (scora.models.blocks.BlocksConfig): The config object
        substack_name (str): The substack name -- its LogicalResourceId or \
            the name it was given on the template


    Returns:
        PhysicalResourceId (str): the PhysicalResourceId for the substack to \
            be used on further queries on props, outputs, etc.
    """
    try:
        # Checks if the stack exists
        stacks = cloudformation.describe_stack_resources(
            StackName=config.project.key)
        stack_resources = stacks.get("StackResources", [])
    except Exception:
        click.echo(f"Stack `{config.project.key}` doesn't seem to exist "
                   f"on `{config.project.region}`")
        sys.exit()

    efs_substack = [x for x in stack_resources
                    if x["LogicalResourceId"] == substack_name]

    if not efs_substack:
        click.echo(f"Stack `{config.project.key}` doesn't seem to have "
                   f"the {substack_name} where it should be")
        sys.exit()

    return efs_substack[0].get("PhysicalResourceId").split("/")[1]


def get_cfn_resource_prop(
        cloudformation, stack_id, attr, attr_val, res_prop):
    """Generic query on a cloudformation stack to get its resourcesprops.
    Understand as if we're doing:
    `select res_prop from stack_id where attr = attr_val`

    Args:
        cloudformation (CloudFormation.Client): The cloudformation client
        stack_id (str): The id of the stack we're searching into
        attr (str): The resource attribute we want to use for filtering
        attr_val (str): The resource attribute value we want to restrict
        res_prop (str): The resources property we want to retrieve

    Returns:
        [type]: [description]
    """
    try:
        stack_resources = cloudformation.describe_stack_resources(
            StackName=stack_id).get("StackResources", [])
        resource = [x for x in stack_resources if x[attr] == attr_val]
        resource = resource[0]
        return resource.get(res_prop, None)

    except Exception:
        click.echo("Couldn't get the EFS Filesystem from the stack "
                   f"with the name{stack_id}")


def get_cfn_stack_prop(
        cloudformation, stack_id, attr_path, filter_var, filter_value):
    """Generic query on a cloudformation stack to get an attribute value.
    Understand as if we're doing:
    `select attr_path from stack_id where filter_var = filter_value`
    filter_var and filter_value are useful when searching in arrays such as
    Outputs and Parameters for a specific key

    Args:
        cloudformation (CloudFormation.Client): The cloudformation client
        stack_id (str): The id of the stack we're searching into
        attr_path (str): The stack attribute we want to retrieve
        filter_var (str): The attribute[] var we want to use for filtering
        filter_value (str): The attribute[] var value we want to filter

    Returns:
        str: The desired attribute
    """
    try:
        stack = cloudformation.describe_stacks(
            StackName=stack_id).get("Stacks", [])
        if not stack:
            click.echo(
                f"The stack `{stack_id}` doesn't seem to exist on this region")
        stack = stack[0]
        attr = stack.get(attr_path, [])
        if not isinstance(attr, list):
            return attr
        elif isinstance(attr, list) and filter_var and filter_value:
            return next(
                x for x in attr if x[filter_var] == filter_value)

    except Exception:
        click.echo(f"Couldn't get the stack attribute `{attr_path}` using "
                   f"stack[{filter_var}]=`{filter_value}` from {stack_id}")


def get_stack_bucket(cloudformation, stack_id):
    """Rreturns the PRJBUCKET (Project Bucket) for a given stack_id

    Args:
        cloudformation (CloudFormation.Client): The cloudformation client
        stack_id (str): The id of the stack we're searching into

    Returns:
        str: The bucket name
    """
    return get_cfn_stack_prop(
        cloudformation,
        stack_id, "Parameters", "ParameterKey",
        "PRJBUCKET").get("ParameterValue")


def create_airflow_access_point(efs, efs_fs_id, key):
    """Given the key/type, reates an airflow access point on a given EFS
    Filesystem

    Args:
        efs (EFS.Client): The EFS boto3 Client
        efs_fs_id (str): The EFS Filesystem ID
        key (str): 'dags' or 'requirements'

    Returns:
        (dict): Newly created access poiont
    """
    return efs.create_access_point(
        Tags=[{
            "Key": "Name",
            "Value": key
        }],
        FileSystemId=efs_fs_id,
        PosixUser={
            "Uid": 1000,
            "Gid": 1000
        },
        RootDirectory={
            "Path": f"/{key}"
        }
    )


def ecs_get_latest_taskrev(ecs, family):
    """Gets the latest task revision for a given ECS Taskdefinition Family

    Args:
        ecs (ECS.Client): The ECS Client
        family (str): The ECS Taskdefinition Family name

    Returns:
        (str): The latest task definition revision for the given family
    """
    return ecs.list_task_definitions(
        familyPrefix=family, status='ACTIVE', sort='DESC',
        maxResults=1).get("taskDefinitionArns")[0].split(":").pop()


def ecs_get_latest_task_definition(ecs, family):
    """Gets the Taskdefinition full description (dict) of the latest revision
    for a given family

    Args:
        ecs (ECS.Client): The ECS Client
        family (str): The ECS Taskdefinition Family name

    Returns:
        (dict): The Taskdefinition full description
    """
    rev = ecs_get_latest_taskrev(ecs, family)
    return ecs.describe_task_definition(
        taskDefinition=f"{family}:{rev}").get("taskDefinition")


def get_ecs_volume(key, efs_id, ap_id):
    """Gets the dict structure of a Taskdefinition EFSVolume using Access
    Points and a given key/name

    Args:
        key (str): The name of the volume
        efs_id (str): The EFS Filesystem ID
        ap_id (str): The EFS Access Point ID

    Returns:
        (dict): The dictionary to be used on ECS to add a new volume
    """
    return {
        "name": key,
        "efsVolumeConfiguration": {
            "fileSystemId": efs_id,
            "transitEncryption": "ENABLED",
            "authorizationConfig": {
                "accessPointId": ap_id,
                "iam": "ENABLED"
            }
        }
    }


def get_ecs_taskdef_register_params(latest_taskdef):
    """Prepares a dict of parameters to be expanded as kwargs when registering
    a taskdefinition which is based on an existing one. The existing 
    parameters are based on the arguments of `ecs.register_task_definition`

    Args:
        latest_taskdef (str): The dict that describes the preexisting task \
        definition

    Returns:
        (dict): A dictionary of non null parameters retrieved from the \
            existing task definition.
    """
    params = {
        "taskRoleArn": latest_taskdef.get("taskRoleArn", None),
        "executionRoleArn": latest_taskdef.get("executionRoleArn", None),
        "networkMode": latest_taskdef.get("networkMode", None),
        "placementConstraints": latest_taskdef.get(
            "placementConstraints", None),
        "requiresCompatibilities": latest_taskdef.get(
            "requiresCompatibilities", None),
        "cpu": latest_taskdef.get("cpu", None),
        "memory": latest_taskdef.get("memory", None),
        "tags": latest_taskdef.get("tags", None),
        "pidMode": latest_taskdef.get("pidMode", None),
        "ipcMode": latest_taskdef.get("ipcMode", None),
        "proxyConfiguration": latest_taskdef.get(
            "proxyConfiguration", None),
        "inferenceAccelerators": latest_taskdef.get(
            "inferenceAccelerators", None),
    }
    params = dict(filter(lambda elem: elem[1], params.items()))
    return params


def wait_for_codebuild(codebuild, build_id, msg_ok, msg_fail):
    """Waits and prints the status for a given build ID, showing messages
    when successful or unsuccessful end

    Args:
        codebuild (Codebuild client): the boto3 Codebuild client
        build_id (str): the build id
        msg_ok (str): The message to show when the build is successful
        msg_fail (str): The message to show when the build is not successful
    """
    while True:
        time.sleep(3)
        build_status = codebuild.batch_get_builds(
            ids=[build_id]).get("builds")[0]

        click.echo(
            f"Build id {build_id} "
            f"current phase: {build_status['currentPhase']} "
            f"current status: {build_status['buildStatus']}")

        if build_status["buildStatus"] != "IN_PROGRESS":
            if build_status["buildStatus"] == "SUCCEEDED":
                click.echo(msg_ok)
            else:
                click.echo(msg_fail)
            break


def stack_exists(cloudformation, name):
    """Checks whether a stack with a given name exists or not

    Args:
        name (str): The stack name
        required_status (str, optional): Defaults to 'CREATE_COMPLETE'.

    Returns:
        (bool): Whether a stack with a given name exists or not
    """
    try:
        data = cloudformation.describe_stacks(StackName=name)
    except ClientError:
        return False
        
    return True
