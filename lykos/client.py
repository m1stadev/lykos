from importlib.metadata import version
from typing import List, Optional

from loguru import logger
from requests import Session

from .errors import PageNotFound
from .types import Component

HEADERS = {
    'User-Agent': f'lykos/{version(__package__)}'
}

BASE_URL = 'https://theapplewiki.com'

class Client:
    def __init__(self) -> None:
        self._session = Session()

    def _find_page_title(self, search: str) -> str:
        params = {
            'action': 'query',
            'format': 'json',
            'list': 'search',
            'srsearch': search,
            'srwhat': 'title',
            # Keys namespace
            'srnamespace': 2304,
            'srlimit': 1,
        }

        logger.debug(f'Finding page title from search: "{search}"')
        data = self._session.get(BASE_URL + '/api.php', headers=HEADERS, params=params).json()
        if data['query']['searchinfo']['totalhits'] == 0:
            raise PageNotFound(f'No pages found from search: "{search}"')
        
        return data['query']['search'][0]['title']

    def _fetch_key_data(self, title: str) -> dict:
        ask_query = f'[[-Has subobject::{title}]]'
        ask_query += '|?Has filename=filename'
        ask_query += '|?Has key=key'
        ask_query += '|?Has key IV=iv'

        params = {
            'action': 'ask',
            'format': 'json',
            'query': ask_query,
            'api_version': 2
        }

        logger.debug(f'Fetching key data from title: "{title}"')
        data = self._session.get(BASE_URL + '/api.php', headers=HEADERS, params=params).json()
        if len(data['query']['results']) == 0:
            raise PageNotFound(f'No wiki pages found from title: "{title}"')

        return data

    def _parse_key_data(self, data: dict) -> List[Component]:
        components = []
        for key, value in data['query']['results'].items():
            name = key.split('#')[-1]

            if len(value['printouts']['iv']) == 0:
                logger.debug(f'No IV found for component: {name}, skipping')
                continue

            if value['printouts']['iv'][0]['fulltext'] in ('Not Encrypted', 'Unknown'):
                logger.debug(f'Component: {name} is not encrypted, skipping')
                continue

            key = bytes.fromhex(value['printouts']['key'][0]['fulltext'])
            iv = bytes.fromhex(value['printouts']['iv'][0]['fulltext'])

            component = Component(name=name, key=key, iv=iv)
            logger.debug(f'Found component: {component}')
            components.append(component)

        logger.debug(f"Found {len(components)} component{'s' if len(components) != 1 else ''}")
        return components


    def get_key_data(self, device: str, buildid: str, codename: Optional[str]=None) -> List[Component]:
        if codename:
            logger.info(f'Fetching key data for device: {device}, buildid:{buildid}, codename:{codename}')
            title = f'Keys:{codename} {buildid} ({device})'
        else:
            logger.info(f'Fetching key data for device: {device}, buildid:{buildid}')
            title = self._find_page_title(search=f'{device} {buildid}')

        key_data = self._fetch_key_data(title=title)
        return self._parse_key_data(data=key_data)

