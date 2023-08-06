sallron |PyPI version fury.io| |PyPI pyversions|
================================================

    Dynamically schedule data aggregation ⚔️ 👁️ 🗄️

API agnostic data aggregation scheduler that automatically interacts
with your interface class and sends responses to DB.

Dependencies
^^^^^^^^^^^^
-  requests
-  schedule
-  pymongo
-  walrus
-  psutil
-  pytz
-  discord-logger
-  boto3

Setup
~~~~~

.. code:: bash

    pip3 install sallron

DB Structure
~~~~~~~~~~~~

To do

Usage
~~~~~

If you want a regular lifecycle, just run the following code:

.. code:: python

    import sallron
    import ExampleInterface

    sallron.configureye(
        MONGO_CONN_STR='mongodb+srv://...',
        MAX_STEEL_URL='https://5423csd3j.exe...',
        ADMIN_COLLECTION='admin',
        _WEBHOOK='https://discord.com/api/webhooks/...', # Discord webhook for logging
        # AWS CONFIG
        AWS_ACCESS_KEY_ID="asnwnwjsMANS...",
        AWS_SECRET_ACCESS_KEY_ID="JASDWKkjndm$234/mkasd...",
        AWS_REGION="us-east-2", # default
        LOGGING_BUCKET='s3 bucket name for storing logs'
    ) # configure your MongoDB settings
    
    sallron.ring_ruler(ExampleInterface, "my_interface")

Now, for auto-resets + notifications on exceptions/crashes, save the
previous file as you normally would (i.e. runner.py) and create a new
file (i.e. erunner.py):

.. code:: python

    from sallron import eternal_runner
    from os.path import join, dirname

    here = dirname(__file__)

    if __name__ == "__main__":
        filename = "runner.py"
        filepath = join(here, filename)
        eternal_runner(filepath)

Then just:

.. code:: shell

    python3 erunner.py

Configureye
~~~~~~~~~~~

Required settings:

-  MONGO\_CONN\_STR
-  ADMIN\_COLLECTION

Available settings (= std\_value):

-  OS = 'UBUNTU'
-  SAVE\_LOGS = False
-  LOG\_DIR = "logs/"
-  MAX\_LOG\_SIZE = 100000000 # 100Mb

.. |PyPI version fury.io| image:: https://d25lcipzij17d.cloudfront.net/badge.svg?id=py&type=6&v=0.0.9&x2=0
   :target: https://github.com/elint-tech/sallron
.. |PyPI pyversions| image:: https://img.shields.io/pypi/pyversions/sallron
   :target: https://github.com/elint-tech/sallron
