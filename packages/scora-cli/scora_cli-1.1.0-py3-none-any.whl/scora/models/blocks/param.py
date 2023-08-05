import yaml


class Param(yaml.YAMLObject):
    """Represents a configuration parameter that has an environment variable
    to be forwarded to Scora Blocks, a value type and the actual value.
    The value type is useful for formatting the output to
    docker.

    Args:
        var (str): The name of the environment variable to store the value \
            when forwarding to scora blocks
        value (any): The actual value that should be stored
        val_type (str): The value type, one of "str", "bool", "int"

    Attributes:
        var (str): The name of the environment variable that will forward the \
        value to scora blocks
        value (any): The actual value that should be stored
        val_type (str): The type of the value that is stored
    """

    yaml_loader = yaml.SafeLoader
    yaml_tag = u'param'

    def __init__(self,
                 var=None,
                 value=None,
                 val_type="bool",):
        self.var = var
        self.value = value
        self.val_type = val_type

    def set_var(self, var):
        """Sets the variable name

        Args:
            var (str): The environment variable name that will be used in \
                Scora Blocks
        """
        self.var = var

    def set_value(self, value):
        """Sets the parameter value

        Args:
            value (any): The value to be stored
        """
        self.value = value

    def set_val_type(self, val_type):
        """Sets the parameter value type

        Args:
            val_type (str): The type of the value that is stored into `value`.\
                one of "str", "bool", "int"

        """
        self.val_type = val_type
