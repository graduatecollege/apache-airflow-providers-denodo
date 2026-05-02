__version__ = "1.0.0"



## This is needed to allow Airflow to pick up specific metadata fields it needs for certain features.
def get_provider_info():
    return {
        "package-name": "denodo-airflow-provider",  # Required
        "name": "denodo",  # Required
        "description": "A sample template for Apache Airflow providers.",  # Required
        "connection-types": [
            {
                "connection-type": "denodo",
                "hook-class-name": "denodo_airflow_provider.hooks.denodo.DenodoHook"
            }
        ],
        "versions": [__version__],  # Required
    }
