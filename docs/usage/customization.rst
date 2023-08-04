Customization
=====

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
