import yaml
from .param import Param


class Project(yaml.YAMLObject):
    """
    Stores the project configuration. A project has metadata about the project
    itself and its deployment environment.

    Args:
        name (string, optional): The project friendly name
        key (string, optional): The project unique key -- must be unique \
            across the cloud account that the stack will be deployed
        region (string, optional): The region where the stack should be \
            deployed
        templates_bucket (string, optional): The bucket that is temporarily \
            going to store the stack tamplates while it's being deployed

    Attributes:
        name (string, optional): The project friendly name
        key (string, optional): The project unique key -- must be unique \
            across the cloud account that the stack will be deployed
        region (string, optional): The region where the stack should be \
            deployed
        templates_bucket (string, optional): The bucket that is temporarily \
            going to store the stack tamplates while it's being deployed
    """

    yaml_loader = yaml.SafeLoader
    yaml_tag = u'project'

    def __init__(self,
                 name=None,
                 key=None,
                 region=None,
                 templates_bucket=None):

        self.name = Param(var='PRJNAME', value=name)
        self.key = Param(var='PRJKEY', value=key)
        self.region = Param(var='PRJREGION', value=region)
        self.templates_bucket = Param(var='TEMPLATESBUCKET',
                                      value=templates_bucket)

    def set_name(self, name):
        """Sets the project name

        Args:
            name (str): The project friendly name
        """
        self.name = name

    def set_region(self, region):
        """Sets the project region

        Args:
            region (str): The region where the stack should be deployed
        """
        self.region = region

    def set_key(self, key):
        """Sets the project key

        Args:
            key (str): The project unique key -- must be unique \
            across the cloud account that the stack will be deployed
        """
        self.key = key

    def set_templates_bucket(self, templates_bucket):
        """Sets the project templates bucket

        Args:
            templates_bucket (str): The bucket that is temporarily \
            going to store the stack tamplates while it's being deployed
        """
        self.templates_bucket = templates_bucket
