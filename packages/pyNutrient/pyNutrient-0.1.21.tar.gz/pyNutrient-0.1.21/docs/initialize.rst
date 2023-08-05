Initialization of a new Project
==================================

Introduction
--------------
This tutorial documents my workflow for creating a new project from scratch, and creates  a documented, version-controlled, pip-intsallable module with an automated build, test, and deploy pipeline.

Setting up Github Repository and Development Pipeline
--------------------------------------------------------
#. Initialize and setup a new github repository 
   
   - Add .gitignore, .environment.yml, LICENSE.txt, MANIFEST.in, README.md, .coveragerc, and setup.py files to main directory (can copy these from other directory)
   - Modify the module names / paths for each of these files: README.md, setup.py
   - Create a new github repository
   - Add the github repository remote with: :code:`git remote add origin main` followed by :code:`git remote origin set-url <URL>`. 
   - Modify conf.py and setup.py to contain your project-specific information
   - Create subdirectory with your module name, and directories inside that called 'docs', 'source', and 'test'.
   - Copy all docs files from a previous project

#. Setup test suite, codebase
   - Copy context.py files from the source, test, and main directories
   - Copy fullRunner.py, single test file from test directory
   - Copy shorthandTest.py file from test directory
   - Create basic test and try to run fullRunner.py using coverage: :code:`coverage run fullRunner.py`

#. Upload repository to test pyPi and pyPi

   - Attempt to build install files: :code:`python setup.py sdist bdist_wheel`
   - run :code:`twine upload --repository testpypi dist/*`, put in your username / password
   - Create a new authentication key on test PyPi for the project you just uploaded
   - Create a github secret :code:`pypi_test_password` in your new repository
   - run :code:`twine upload --repository pypi dist/*`, put in your username / password
   - Create a new authentication key on test PyPi for the project you just uploaded
   - Create a github secret :code:`pypi_test_password` in your new repository

#. Setup documentation 
   - Configure github pages source in the "Settings" section of the repository to be the "/docs" folder.

#. Setup github actions

   - Create .github/workflows/ directory in root directory
   - Move .yml file from previous project into that directory
   - Change .yml file references to your module name
   - Attempt to lint main directory by running :code:`flake8`
   - Push to github and check that all actions run

#. Setup stickers

   - Go to `coveralls <https://coveralls.io/>`_ and add your repository
   - Change the markdown file for your github build to whatever the name of your repository is


