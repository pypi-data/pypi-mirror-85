=====
Usage
=====

To use SICOR in a project::

    import sicor


Quickstart
----------

For processing multispectral data, atmospheric fields from ECMWF for your time of interest should be downloaded:

.. code-block:: console

    sicor_ecmwf.py --help


If this data is missing, SICOR can fall-back to default values, but this approach is not recommended.


Using SICOR from python:


.. code-block:: python

    # for multispectral data
    from sicor import AC
    AC()

.. code-block:: python

    # for hyperspectral data
    from sicor.sicor_enmap import sicor_ac_enmap
    enmap_l2a_vnir, enmap_l2a_swir, cwv_model, cwc_model, ice_model, toa_model, se, scem, srem = sicor_ac_enmap(data_l1b, options, logger)


From command line (currently, only applicable to the multispectral case):

.. code-block:: console

    sicor_ecmwf.py --help
    sicor_ac.py --help


Command line utilities
-----------

At the command line, sicor provides the **sicor_ac.py** command for multispectral datasets:

.. argparse::
   :filename: ./../bin/sicor_ac.py
   :func: sicor_ac_parser
   :prog: sicor_ac.py

The command line utility for hyperspectral datasets is currently under development


The program **sicor_ecmwf.py** can be used to download needed products from ECMWF servers needed for processing
multispectral datasets:

.. argparse::
   :filename: ./../bin/sicor_ecmwf.py
   :func: sicor_ecmwf_parser
   :prog: sicor_ecmwf.py


Makefile
--------

SICOR operations can be started using make, available options are:

 .. code-block:: console

    $ make

    make options: (run make [option] to perform action):

    clean:
        Remove all build, test, coverage and Python artifacts.

    clean-build:
        Remove build artifacts including build/ dist/ and .eggs/ folders.

    clean-pyc:
        Remove Python file artifacts, e.g. pyc files.

    clean-test:
        Remove test and coverage artifacts.

    convert_examples_to_doc:
        Use nbconvert to convert jupyter notebooks in examples to doc/examples.
        Links to internal images are adjusted such that SPHINX documentation
        can be build.

    coverage:
        Use coverage to run tests and to produce a coverage report.

    coverage_view:
        Open default browser to check coverage report.

    docs:
        Generate HTML documentation using SPHINX. If example jupyer notebooks
        should be updated, run the target 'convert_examples_to_doc'
        first.

    download-tables (currently, only needed for multispectral case):
        Download tables for atmospheric correction and scene classification
        from google drive if not found locally (anywhere in $PATH). Gdrive
        might be unreliable and fail. Just try again later. Files are
        checked for their hash before continuing here.

    download-tables-all (currently, only needed for multispectral case):
        Download ALL tables for atmospheric correction and scene classification.
        This includes additional data, e.g. for methane retrievals or
        further development.

    examples_notebooks:
        Start a jupyter notebook server in the examples directory and
        open browser.

    gitlab_CI_docker:
        Build a docker image for CI use within gitlab. This is based
        on docker and required sudo access to docker. Multiple images
        are build, the 'sicor:latest' includes a working environment
        for SICOR and is used to run the tests. SICOR is not included
        in this image and it is cloned and installed for each test run.

    install:
        Install the package to the active Python site-packages.

    lint:
        Check style and pep8 conformity using multiple pep8 and style
        checkers. Flake8 and pycodestyle need to complete without error
        to not fail here. For now, pylint and pydocstyle are included,
        but their results ignored. The target 'test' depends on 'lint'
        which means that testing can only be a success when linting was
        run without errors. Run this before any commit!

    nose2:
        Run all tests using nose2. Coverage and other plugins are included
        in the ini settings file.

    nose2_debug:
        Run a single test using nose2. This is useful for debugging.
        Change this if needed.

    requirements:
        Install requirements as defined in requirements.txt using pip.

    test:
        Run tests quickly with the default Python interpreter and without
        coverage.

    test_single:
        Run a single test quickly with the default Python and without
        coverage. This is useful for debugging errors and feel free to
        change the considered test case to your liking.
