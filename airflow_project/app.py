# A CONSERVER

from dotenv import load_dotenv
import os
import logging

# Charger les variables d'environnement à partir du fichier .env
load_dotenv()

# Utiliser les variables d'environnement
executor = os.getenv('AIRFLOW__CORE__EXECUTOR')
sql_alchemy_conn = os.getenv('AIRFLOW__CORE__SQL_ALCHEMY_CONN')
fernet_key = os.getenv('AIRFLOW__CORE__FERNET_KEY')
secret_key = os.getenv('AIRFLOW__WEBSERVER__SECRET_KEY')
acr_username = os.getenv('ACR_USERNAME')
acr_password = os.getenv('ACR_PASSWORD')

logging.basicConfig(level=logging.INFO)


def main():
    logging.info("Script started")
    try:
        # Votre code ici
        print("Hello, World!")
    except Exception as e:
        logging.error(f"An error occurred: {e}")


if __name__ == '__main__':
    main()
    logging.info("Script finished")

#az container create --resource-group ressource_cac40 --name mycac40container --image containercac40registry.azurecr.io/cac40container:latest --cpu 2 --memory 4 --registry-login-server containercac40registry.azurecr.io --registry-username containercac40registry --registry-password mXLPDTLdIhCxnZ2nzjdUt6xe1WIJVjWA5dVpqDn0ld+ACRCgFuMT --dns-name-label mycac40container --ports 8000
