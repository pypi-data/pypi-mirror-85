import yaml
import io
import json
from .project_config import Project
from .resource_config import Resource

DEFAULT_DOCKER_IMG = (
    "oncase/scora-blocks"
    "@sha256:a3993f39dedbaf1973f0399af8f7881078866798456422aaf63b09ebe09cda5a")

resources_map = {
    "bucket": {
        "create": {"key": "HASBUCKET", "type": "bool"},
        "bucket": {"key": "PRJBUCKET",  "type": "str"}
    },
    "domain": {
        "create": {"key": "HASDOMAIN", "type": "bool"},
        "domain": {"key": "DOMAIN", "type": "str"},
    },
    "athena": {
        "create": {"key": "HASATHENA", "type": "bool"},
    },
    "efs": {
        "create": {"key": "HASEFS", "type": "bool"},
        "dags_ap_id": {"key": "EFSDAGSID", "type": "str"},
        "reqs_ap_id": {"key": "EFSREQID", "type": "str"},
    },
    "rds": {
        "create": {"key": "HASRDS", "type": "bool"},
        "instance_type": {"key": "RDSINSTANCETYPE", "type": "str"},
    },
    "airflow": {
        "create": {"key": "HASAIRFLOW", "type": "bool"},
        "start": {"key": "STARTAIRFLOW", "type": "bool"},
        "taskrev": {"key": "AIRFLOWTASKREV", "type": "int"},
    },
    "metabase": {
        "create": {"key": "HASMETABASE", "type": "bool"},
        "start": {"key": "STARTMETABASE", "type": "bool"},
    },
    "identity": {
        "create": {"key": "HASIDENTITY", "type": "bool"},
    },
    "frontend": {
        "create": {"key": "HASFRONTEND", "type": "bool"},
    },
    "sandboxing": {
        "create": {"key": "HASSANDBOXING", "type": "bool"},
        "repo": {"key": "PRJREPO", "type": "str"},
        "branch": {"key": "NOTEBOOKSBRANCH", "type": "str"},
    },
    "redshift": {
        "create": {"key": "HASREDSHIFT", "type": "bool"},
    },
    "extension": {
        "create": {"key": "HASEXTENSION", "type": "bool"},
    },
}  # : Notice the colon,


class BlocksConfig(yaml.YAMLObject):
    """
    Stores the blocks config into a YAML serializable format.
    Creates an empty or deserialized representation of a Blocks Config.

    Args:
        conf_file (string, optional): Optional file path from which the
                class will attempt to deserialize a YAML Representation.
                Defaults to None.

    Attributes:
        project (Project): Project configuration
        resources (:obj:`list` of Resource): List of resources \
            configurations

    """

    yaml_loader = yaml.SafeLoader
    yaml_tag = u'blocks'

    resources_map = resources_map  #: Dictionary of supported resources+Vars

    def __init__(self, conf_file=None):
        if conf_file:
            self.deserialize_from_file(conf_file)

        else:
            self.project = Project()
            self.resources = {}
            self.docker_img = None

    def add_resource(self, key):
        """Adds a resource to the configuration.
        A resource represents a cloud resource that initially only has
        the `create` attribute populated.

        Args:
            key (str): The resource key; must be an implemented type of \
            resource mapped in `resources_map`;

        Raises:
            Exception: Tried to add a resource that is not mapped

        Returns:
            resource (Resource): the newly created resource
        """
        if key not in resources_map:
            raise Exception("Tried to add a resource that is not mapped")

        self.resources[key] = Resource(
            key=key,
            create_var=resources_map[key]["create"])
        return self.resources[key]

    def set_resource_param(self, resource_key, param_key, value=None):
        """Sets a resource param value given its resource_key, the param key
        and its value

        Args:
            resource_key (str): Cloud resource key -- must be an \
                                     implemented type
            param_key (str): Resource parameter key -- must be an \
                                     implemented param for the resource
            value (any, optional): Value to be stored. Defaults to None.

        Raises:
            Exception: Attempted to add non existing parameter
        """
        resource = self.resources.get(resource_key, None)
        param_conf = resources_map[resource_key][param_key]

        if not resource:
            resource = self.add_resource(resource_key)

        if not param_conf:
            raise Exception("Attempted to add non existing parameter")

        resource.set_param(
            key=param_key,
            var=resources_map[resource_key][param_key]["key"],
            val_type=resources_map[resource_key][param_key]["type"],
            value=value
        )

    def serialize_to_file(self, filename):
        """Serializes an object representation of this class to a given file.

        Args:
            filename (str): File path where to serialize the object.
        """
        with open(filename, 'w') as outfile:
            yaml.dump(self, outfile, default_flow_style=False, indent=4)

    def deserialize_from_file(self, filename):
        """Deserializes the contents of a yaml serialized BlocksConfig
        into an instance of this class.

        Args:
            filename (str): The file path to read from.
        """
        with io.open(filename, 'r') as strm:
            values = yaml.safe_load(strm)
            self.project = values.project
            self.resources = values.resources
            if hasattr(values, "docker_img"):
                self.docker_img = values.docker_img
            else:
                self.docker_img = DEFAULT_DOCKER_IMG

    def get_stack_vars(self):
        """Formats all the supported resources parameters into a dict format
        mapped with its var names.

        Returns:
            variables (dict): Dictionary of environment-vars : values of the \
            supported resources parameters.
        """
        vars = {
            "PRJKEY": self.project.key,
            "PRJNAME": self.project.name,
            "PRJREGION": self.project.region,
            "TEMPLATESBUCKET": self.project.templates_bucket
        }
        for key, resource in self.resources.items():
            ref_resource = resources_map[key]
            for ref_key, ref_attrs in ref_resource.items():
                attr = getattr(resource, ref_key, None)
                if attr:
                    if(attr.val_type == "bool"):
                        vars[attr.var] = "true" if attr.value else "false"
                    else:
                        vars[attr.var] = attr.value
        return vars
