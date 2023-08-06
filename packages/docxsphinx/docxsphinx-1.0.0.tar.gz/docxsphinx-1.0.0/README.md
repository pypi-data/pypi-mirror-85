# DocxSphinx

[![CircleCI](https://circleci.com/gh/mherkazandjian/docxsphinx/tree/master.svg?style=svg)](https://circleci.com/gh/mherkazandjian/docxsphinx/tree/master)

Introduction
============
This repository has been forked from

   https://bitbucket.org/shimizukawa/sphinxcontrib-docxbuilder

and some heavy modification have been done. The major changes are listed in
the release notes (`todo` add the release notes).

Installation
============
The latest bleeding edge version can be installed through

   ```
   pip install docxsphinx
   ```

To install the development version

   ```
   pip install git+https://github.com/mherkazandjian/docxsphinx.git@master
   ```

Alternatively the repository can be cloned and installed locally

   ```
   git clone https://github.com/mherkazandjian/docxsphinx.git
   cd docxsphinx
   python -m pip install -r requirements.txt
   python setup.py install
   ```

After installation, ```make docx``` in a sphinx project  should work
(see next section)

Generating a `docx` document
============================
It is assumed that a sphinx project already is in place. At least one change
must be done to `conf.py` in-order to be able to generate a docx file.

The following line must be added to `conf.py`:

   ```
   extensions = ['docxsphinx']
   ```

The sample projects are in the directory `examples`

  - REPO_ROOT/examples/sample_1 : default example (from the original repo)
  - REPO_ROOT/examples/sample_2 : example tested with `make docx`
  - REPO_ROOT/examples/sample_3 : example tested with `make docx` with a custom style


Word styles
===========

a custom word style file can be specified by adding

    ```
    # 'docx_template' need *.docx or *.dotx template file name. default is None.
    docx_template = 'template.docx'
    ```

to the end of `conf.py` (or anywhere in the file)

Development
===========

Setup the development environment (make sure that pipenv is installed):

   ```
   pipenv install --dev        # creates the .venv dir
   pipenv shell                # set the environment to use the venv 
   python setup.py install
   make tests -B
   ```

whenever changes are made the package needs to be re-installed through:

   ```
   python setup.py install
   ```

since the tests are run using the commands ``sphinx-build`` that needs to be
in the environment paths.

The tests can also be run using (but this is not recommended and will be
removed in the future):

   ```
   python setup.py test
   ```
 
To debug the build process

   ``` 
   python -m pdb $(which sphinx-build) -b docx /path/to/src/dir /path/to/build/dir OTHER_SPHINX_OPTIONS_IF_ANY
   ```

To produce the ``.docx`` of any of the example files using the current
development docxsphinx source, e.g. the sphixn project ``sample_2``:

   ```
   cd examples/sample_2
   PYTHONPATH=../../src:$PYTHONPATH make docx -B
   ```

Profiling is useful to see which sections of the code are 
visited in the module ``src/docxsphinx/writer.py``. For example
to profile ``sample_2``, the following pattern can be used:

   ```
   PYTHONPATH=../../src:$PYTHONPATH python3 -m cProfile -s calls $(which sphinx-build) -M docx source build/docx/ | grep writer.py | awk '{print $6}' | sort > calls
   ```

API
===
see also 

    REPO_ROOT/src/README.md  (outdated - but useful)
    REPO_ROOT/src/docxsphinx/docx/README.md
