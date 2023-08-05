Scora CLI
=============================

This CLI is coupled with the Idea of the Scora Platform and Scora Blocks to:

* Configure Cloud Stacks removing the complexity of writing templates;
* Helping on CI/CD projects with the Airflow on the architecture defined by Scora Blocks;
* Helping configuring repositories for fullstack apps that use Cognito, CloudFront, S3 and Lambda;


Development
-----------------------------

Testing before building
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


.. code-block:: bash

    # Configure the dependencies
    virtualenv -p python3
    . ./venv/bin/activate
    pip install -e .[dev]

    # run init
    python -c 'from scora.commands.blocks.impl import init; init()'

    # run push
    python -c 'from scora.commands.blocks.impl import push; push()'




Build, install, test locally
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    # build from this source -- considering that dependencies are resolved
    rm -rf ./dist/* && python3 setup.py sdist bdist_wheel

    # From another venv -- install 
    virtualenv -p python3
    . ./venv/bin/activate
    pip install <REPO_HOME>/dist/scora-cli-0.1.0.tar.gz 


    # Run fr
    scora --help 




Build the docs
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


.. code-block:: bash

    # build -- considering that dependencies are resolved
    rm -rf ./docs_build && make html
    open ./docs_build/html/index.html 
