import click
from . import impl


@click.group()
def blocks():
    """
    Helps create, update and maintain your project infrastructure
    """
    pass


@blocks.command('init')
@click.option('--profile', '-p', type=str,
              default=None, help="AWS profile to use")
@click.option('--dir', '-d', default=None, type=str,
              help="Directory where the blocks.yaml will be stored or loaded")
@click.option('--templates-bucket', '-tb', default='oncase-prj-templates',
              type=str, help="Bucket to temporary hold the Cloudformation \
                  templates. Defaults to `oncase-prj-templates`")
def init(profile, dir, templates_bucket):
    """
    Helps create the boilerplate of your project infrastructure
    """
    impl.init(profile, dir, templates_bucket)


@click.option('--profile', '-p', type=str,
              default=None, help="AWS profile to use")
@click.option('--dir', '-d', default=None, type=str,
              help="Directory from where to read the blocks.yaml")
@click.option('--templates-bucket', '-tb', default='oncase-prj-templates',
              type=str, help="Bucket to temporary hold the Cloudformation \
                   templates")
@blocks.command('push')
def push(profile, dir, templates_bucket):
    """Pushes (creates or updates) infrastructure stack to Cloudformation"""
    impl.push(profile, dir, templates_bucket)


@click.option('--profile', '-p', type=str,
              default=None, help="AWS profile to use")
@click.option('--dir', '-d', default=None, type=str,
              help="Directory from where to read the blocks.yaml")
@blocks.command('delete')
def delete(profile, dir):
    """Deletes the stack referenced from within the <dir>/blocks.yaml"""
    impl.delete(profile, dir)


@click.option('--profile', '-p', type=str,
              default=None, help="AWS profile to use")
@click.option('--dir', '-d', default=None, type=str,
              help="Directory from where to read the blocks.yaml")
@blocks.command('mount-efs-to-airflow')
def efs_mount(profile, dir):
    """Mounts the efs drive to airflow"""
    impl.efs_mount(profile, dir)
