import yaml
from .param import Param


class Resource(yaml.YAMLObject):
    """
    Stores the configuration of a generic resource. The implemented resources
    and attributes are determined in
    :attr:`~scora.models.blocks.blocks_config.BlocksConfig.resources_map`

    Args:
        conf_file (string, optional): Optional file path from which the
                class will attempt to deserialize a YAML Representation.
                Defaults to None.

    Attributes:
        project (Project): Project configuration
        resources (:obj:`list` of Resource): List of resources \
            configurations.
    """

    yaml_loader = yaml.SafeLoader
    yaml_tag = u'resource'

    def __init__(self,
                 key,
                 create_var):

        self.create = Param(
            var=create_var,
            value=False)

    def set_param(self, key, var=None, value=None, val_type=None):
        """Sets a generic parameter on the resource.

        Args:
            key (str): The parameter key
            var (str): The parameter environment variable to be used \
                with Scora Blocks
            value (any): The value to be stored
            val_type (str): The type of the value that is going to be stored
        """
        setattr(self, key, Param(
            var=var,
            value=value,
            val_type=val_type
        ))
