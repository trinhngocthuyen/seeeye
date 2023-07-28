Usage
=====

Using CLI
---------

Following are some CLI examples to work with iOS projects. Make sure you are running those commands in the root directory of the iOS project (ie. the one having ``.xcworkspace`` or ``.xcodeproj`` file).

To build the project

.. code-block:: console

    $ cicd ios build

To test the project

.. code-block:: console

    $ cicd ios test

To build the project for testing, then test without building

.. code-block:: console

    $ cicd ios build --build-for-testing
    $ cicd ios test --test-without-building

To archive the project

.. code-block:: console

    $ cicd ios archive --profiles <app_bundle_id>:<provisioning_profile_name>

.. note::

    To see the usage of the CLI, run with the argument ``--help``. Example: ``cicd --help``

Customization
-------------

You can create your own Python scripts and use the code from ``seeeye`` package. Then you can make your recipes. Check out :doc:`/api/reference` for more details.

.. code-block:: python

    # Example
    # ---------------------------------
    # Place this code in `scripts/build.py`. Then you can execute it by:
    #     $ `python3 scripts/build.py`
    # ---------------------------------
    from cicd.ios.mixin.build import BuildMixin


    if __name__ == '__main__':
        BuildMixin().start_building(
            configuration='Test',
            derived_data_path='DerivedData',
        )
