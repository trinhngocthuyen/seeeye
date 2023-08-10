Testing the Project
===================

To test the project using the CLI

.. code-block:: console

    $ cicd ios test

.. note::

    To see the usage of the CLI, run with the argument ``--help``. Example: ``cicd --help``

Test Retries
~~~~~~~~~~~~

Sometimes, you might encounter flaky tests which intermittently fail. One common approach to deal with them is to retry failed tests. This toolkit offers a convenient way to achieve that. Simply use the ``--retries`` option in the CLI.

.. code-block:: console

    $ cicd ios test --retries 1


Test Sharding
~~~~~~~~~~~~~

Test sharding means dividing your tests into multiple shards. This is a a common practice to reduce the overall test time on CI by running multiple parallel testing jobs on CI.

To facilitate this feature, use the ``--shards`` and ``--shard-idx`` in the CLI when running tests:

.. code-block:: console

    $ cicd ios test --shards <number-of-shards> --shard-idx <number>

For example, with the following command, ``seeeye`` divides the tests into 3 shards and the 1st shard is picked up for testing.

.. code-block:: console

    $ cicd ios test --test-without-building --shards 3 --shard-idx 1

Assume the project has 5 tests:

- ``TestTarget/TestClass/test1``
- ``TestTarget/TestClass/test2``
- ``TestTarget/TestClass/test3``
- ``TestTarget/TestClass/test4``
- ``TestTarget/TestClass/test5``

Then the above execution runs tests against ``TestTarget/TestClass/test1`` and ``TestTarget/TestClass/test2``.

.. note::

    Tests are sorted alphabetically before being divided into shards.
