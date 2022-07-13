Usage
=====

Using CLI
---------

Following are some CLI examples to work with iOS projects. Make sure you are running those commands in the root directory of the iOS project (ie. the one having ``.xcworkspace`` or ``.xcodeproj`` file).

To build the project

.. code-block:: console

    $ python3 -m cicd.ios.build

To test the project

.. code-block:: console

    $ python3 -m cicd.ios.test

To build the project for testing, then test without building

.. code-block:: console

    $ python3 -m cicd.ios.build --build-for-testing
    $ python3 -m cicd.ios.test --test-without-building

.. note::

    To see the usage of the CLI, run with the argument ``--help``. Example: ``python3 -m cicd.ios.build --help``

.. tip::

    The CLI commands of ``cicd.ios`` are centralized in the ``cicd.ios.cli`` module. This means:

    - Running ``python3 -m cicd.ios.cli build`` is equivalent to ``python3 -m cicd.ios.build``.
    - You can see all available CLI commands under ``cicd.ios`` by running ``python3 -m cicd.ios.cli --help``.


Customization
-------------

You can create your own Python scripts and use the code from ``seeeye`` package. Then you can make your recipes. Check out :doc:`/api/reference` for more details.

.. code-block:: python

    # Example
    # ---------------------------------
    # Place this code in `scripts/build.py`. Then you can execute it by:
    #     $ `python3 scripts/build.py`
    # ---------------------------------
    from cicd.ios.build import BuildJob


    if __name__ == '__main__':
        BuildJob(
            configuration='Test',
            derived_data_path='DerivedData',
        ).run()
