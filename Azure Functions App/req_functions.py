from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from bs4 import BeautifulSoup
import requests


def request_url(url, headers=None, timeout=10, max_retries=3, backoff_factor=0.3):
    '''
    Send a GET request to a specified URL with retries and exponential backoff.

    Arguments
    ----------
    url : str
        The URL to which the GET request will be sent.
    headers : dict, optional
        A dictionary of HTTP headers to send with the request. If not provided, a default 
        User-Agent header is used.
    timeout : int, optional
        The number of seconds to wait for the server to send data before giving up. Default is 10 seconds.
    max_retries : int, optional
        The maximum number of retries allowed if the request fails. Default is 3 retries.
    backoff_factor : float, optional
        A factor that determines the length of time to wait between retries, with exponential backoff. 
        Default is 0.3.

    Returns
    ----------
    BeautifulSoup object or None
        Returns a BeautifulSoup object containing the parsed HTML content if the request 
        is successful. Returns None if the request fails.
    '''
    # Create a session to maintain open connections and handle retries
    session = requests.Session()
    
    # Configure retries with exponential backoff management
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
        response = session.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()  # check statut 
        return BeautifulSoup(response.content, 'html.parser') 
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la requête: {e}")
        return None