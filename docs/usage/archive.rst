Archiving the Project
=====================

To archive the project using the CLI

.. code-block:: console

    $ cicd ios archive

.. note::

    To see the usage of the CLI, run with the argument ``--help``. Example: ``cicd --help``

Code Signing
~~~~~~~~~~~~

Basically, code signing (as part of archiving) requires **a certificate** (with private key) and a **provisioning profiles**. Managing certificates and profiles, especially for CI/CD, is sometimes troublesome. This package offers a convenient way to mange those resources. All you need is the ``cicd ios codesign`` command.

Best Practices
--------------

Encrypting Resources
####################

A common recommendation is to encrypt your certificates and profiles with a *password*. You can commit those encrypted files under your project directory or anywhere else.

.. code-block:: console

    / -- secrets.enc / -- certificate.p12.enc
                       -- profile.mobileprovision.enc

To encrypt such a dir, run the following command:

.. code-block:: console

    $ cicd ios codesign encrypt --password <password> --in <path/to/dir>

Let say you run the above to encrypt files under ``secrets`` dir. Then the encrypted files will be placed under ``secrets.enc``. Those files should also have suffix ``.enc`` to indicates the encryption.

After decrypting them, the files will be placed under ``secrets.dec`` with the suffix ``.enc`` being stripped off.

It is recommended to ignore the decrypted dir from git.

Decrypting Resources
####################

Before using thoses resources, we need to decrypt them. You can use the following command:

.. code-block:: console

    $ cicd ios codesign decrypt --password <password> --in </path/to/encrypted/dir>

Installing Decrypted Resources
##############################

Then, you can install certificates and profiles as follows:

.. code-block:: console

    $ cicd ios codesign prepare --dir <path/to/decrypted/dir>

Combining Decrypting and Installing Resources
#############################################

You can also combine the two steps above (ie. decrypting and installing resources) together:

.. code-block:: console

    $ cicd ios codesign prepare --password <password> --dir <path/to/encrypted/resources>

Cleaning Up Resources
#####################

It is recommended that you clean up the resources on CI if no longer in use.
The following command is to perform the cleanup. This, under the hood, deletes the custom keychain storing the certificates for the archive.

.. code-block:: console

    $ cicd ios codesign cleanup
