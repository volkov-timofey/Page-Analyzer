from bs4 import BeautifulSoup
import requests


def check_url(url: str):
    '''
    Сhecking url address for availability
    '''
    try:
        response = requests.get(url)
    except OSError:
        return None

    if response.status_code in [200, 302]:
        return response

    return None


def parse_html(url: str) -> dict | None:
    '''
    Extracting information from availabily url
    '''
    response = check_url(url)
    if not response:
        return response

    soup = BeautifulSoup(response.content, 'html.parser')

    status_code = response.status_code
    h1 = soup.find("h1").string if soup.find("h1") else ''
    title = soup.find("title").string if soup.find("title") else ''
    description = soup.find(attrs={"name": "description"}).get('content') \
        if soup.find(attrs={"name": "description"}) \
        else ''

    return {
        'status_code': status_code,
        'h1': h1,
        'title': title,
        'description': description,
    }
