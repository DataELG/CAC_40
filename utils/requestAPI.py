from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from bs4 import BeautifulSoup
import requests


def request_url(url, headers=None, timeout=10, max_retries=3, backoff_factor=0.3):
    # Créer une session pour maintenir les connexions ouvertes et gérer les retries
    session = requests.Session()
    
    # Configurer les retries avec gestion de l'attente exponentielle
    retry = Retry(
        total=max_retries,
        read=max_retries,
        connect=max_retries,
        backoff_factor=backoff_factor,
        status_forcelist=[500, 502, 503, 504]
    )
    
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    
    if headers is None:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
        }
    
    try:
        # Effectuer la requête
        response = session.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()  # Vérifier si le statut est 200 (OK)
        return BeautifulSoup(response.content, 'html.parser') # Retourner le contenu de la réponse
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la requête: {e}")
        return None