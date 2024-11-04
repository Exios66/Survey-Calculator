Installation
===========

Prerequisites
------------

Before installing the Survey Calculator, ensure you have the following prerequisites:

* Python 3.8 or higher
* pip (Python package installer)
* Virtual environment tool (optional but recommended)

Installation Steps
----------------

1. Clone the Repository
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   git clone https://github.com/yourusername/survey-calculator.git
   cd survey-calculator

2. Create a Virtual Environment (Optional)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # On macOS/Linux
   python -m venv .venv
   source .venv/bin/activate

   # On Windows
   python -m venv .venv
   .venv\Scripts\activate

3. Install Dependencies
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   pip install -r requirements.txt

Development Installation
----------------------

For development purposes, install additional dependencies:

.. code-block:: bash

   pip install -r requirements-dev.txt

This will install additional packages needed for development:

* pytest - for running tests
* sphinx - for building documentation
* black - for code formatting
* flake8 - for code linting

Configuration
------------

After installation, you'll need to set up your configuration:

1. Copy the example configuration file:

   .. code-block:: bash

      cp config.example.json config.json

2. Edit the configuration file with your preferred settings:

   .. code-block:: json

      {
          "thresholds": {
              "min_score": 0,
              "max_score": 100
          },
          "presets": {
              "default": "standard",
              "available": ["standard", "advanced", "expert"]
          }
      }

Verification
-----------

To verify your installation:

.. code-block:: bash

   python -c "import evaluator; print(evaluator.__version__)"

This should print the version number of the installed package.

Troubleshooting
--------------

Common Issues
~~~~~~~~~~~~

1. **ImportError**: Make sure all dependencies are installed correctly:

   .. code-block:: bash

      pip install --upgrade -r requirements.txt

2. **Permission Errors**: Use sudo (on Unix) or run as administrator (on Windows):

   .. code-block:: bash

      # On Unix
      sudo pip install -r requirements.txt

3. **Version Conflicts**: Try creating a fresh virtual environment:

   .. code-block:: bash

      rm -rf .venv
      python -m venv .venv
      source .venv/bin/activate
      pip install -r requirements.txt

Getting Help
~~~~~~~~~~~

If you encounter any issues:

* Check the `GitHub Issues <https://github.com/yourusername/survey-calculator/issues>`_
* Join our `Discord Community <https://discord.gg/your-invite-link>`_
* Email support at: support@yourproject.com

Updating
--------

To update to the latest version:

.. code-block:: bash

   pip install --upgrade survey-calculator 