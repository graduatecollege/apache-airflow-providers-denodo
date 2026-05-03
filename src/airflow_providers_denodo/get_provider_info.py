# read version from version.txt
from os import path

__version__ = open(path.join(path.dirname(__file__), '_version.txt')).read().strip()

## This is needed to allow Airflow to pick up specific metadata fields it needs for certain features.
def get_provider_info():
    return {
        "package-name": "apache-airflow-providers-denodo",  # Required
        "name": "Denodo",  # Required
        "description": "A simple provider for connecting to Denodo with Apache Airflow.",  # Required
        "integrations": [
            {
                "integration-name": "denodo",
                "external-doc-url": "https://www.denodo.com/",
                "tags": ["software"],
            }
        ],
        "hooks": [
            {
                "integration-name": "denodo",
                "python-modules": ["airflow_providers_denodo.hooks.denodo"],
            }
        ],
        "connection-types": [
            {
                "connection-type": "denodo",
                "hook-class-name": "airflow_providers_denodo.hooks.denodo.DenodoHook",
                "ui-field-behaviour": {"relabeling": {"schema": "Database"}},
            }
        ],
        "asset-uris": [
            {
                "schemes": ["denodo"],
                "handler": "airflow_providers_denodo.assets.denodo.sanitize_uri",
            }
        ],
        "versions": [__version__],  # Required
    }
