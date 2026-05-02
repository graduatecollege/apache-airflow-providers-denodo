# read version from version.txt
from os import path

__version__ = open(path.join(path.dirname(__file__), '_version.txt')).read().strip()

## This is needed to allow Airflow to pick up specific metadata fields it needs for certain features.
def get_provider_info():
    return {
        "package-name": "apache-airflow-providers-denodo",  # Required
        "name": "Denodo",  # Required
        "description": "A simple provider for connecting to Denodo with Apache Airflow.",  # Required
        "connection-types": [
            {
                "connection-type": "denodo",
                "hook-class-name": "denodo_airflow_provider.hooks.denodo.DenodoHook"
            }
        ],
        "versions": [__version__],  # Required
    }
