from importlib.metadata import version
from typing import List, Optional, Tuple

from loguru import logger
from requests import Session

from .errors import PageNotFound
from .types import Component

HEADERS = {'User-Agent': f'lykos/{version(__package__)}'}

BASE_URL = 'https://theapplewiki.com'


class Client:
    def __init__(self) -> None:
        self._session = Session()
        self.components = self._get_component_names()

    def _get_component_names(self) -> Tuple[str]:
        params = {
            'action': 'templatedata',
            'format': 'json',
            # Tenmplate:Keys
            'pageids': '1814',
        }

        logger.debug('Fetching component names')
        data = self._session.get(
            BASE_URL + '/api.php', headers=HEADERS, params=params
        ).json()

        components = []
        for k in data['pages']['1814']['paramOrder']:
            # Skip all '*IV', '*Key', and '*KBAG' keys
            if any(k.endswith(kk) for kk in ('Key', 'IV', 'KBAG')):
                continue

            if any(
                (k + kk) in data['pages']['1814']['paramOrder']
                for kk in ('Key', 'IV', 'KBAG')
            ):
                components.append(k)

        logger.debug(
            f"Found {len(components)} component{'s' if len(components) != 1 else ''}: {', '.join(components)}"
        )
        return tuple(components)

    def _find_page_title(self, search: str) -> str:
        params = {
            'action': 'query',
            'format': 'json',
            'list': 'search',
            'srsearch': f'intitle:{search}',
            # Keys namespace
            'srnamespace': 2304,
            'srlimit': 1,
        }

        logger.debug(f'Finding page title from search: "{search}"')
        data = self._session.get(
            BASE_URL + '/api.php', headers=HEADERS, params=params
        ).json()
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
            'api_version': 2,
        }

        logger.debug(f'Fetching key data from title: "{title}"')
        data = self._session.get(
            BASE_URL + '/api.php', headers=HEADERS, params=params
        ).json()
        if len(data['query']['results']) == 0:
            raise PageNotFound(f'No wiki pages found from title: "{title}"')

        return data

    def _parse_key_data(self, data: dict) -> List[Component]:
        components = []
        for key, value in data['query']['results'].items():
            id_ = key.split('#')[-1]
            logger.debug(f'Finding component name from ID: {id_}')

            for n in self.components:
                logger.debug(f'Comparing: {n.casefold()} == {id_.casefold()}')
                if n.casefold() == id_.casefold():
                    name = n
                    logger.debug(f'Found component name: {name}')
                    break
            else:
                logger.warning(
                    f'No component name found for ID: {id_}, using ID instead'
                )
                name = id_

            if len(value['printouts']['iv']) == 0:
                logger.debug(f'No IV found for component: {name}, skipping')
                continue

            if value['printouts']['iv'][0] in ('Not Encrypted', 'Unknown'):
                logger.debug(f'Component: {name} is not encrypted, skipping')
                continue

            key = bytes.fromhex(value['printouts']['key'][0])
            iv = bytes.fromhex(value['printouts']['iv'][0])

            component = Component(name=name, key=key, iv=iv)
            logger.debug(f'Found component: {component}')
            components.append(component)

        logger.debug(
            f"Found {len(components)} component{'s' if len(components) != 1 else ''}"
        )
        return components

    def get_key_data(
        self, device: str, buildid: str, codename: Optional[str] = None
    ) -> List[Component]:
        if codename:
            logger.info(
                f'Fetching key data for device: {device}, buildid:{buildid}, codename:{codename}'
            )
            title = f'Keys:{codename} {buildid} ({device})'
        else:
            logger.info(f'Fetching key data for device: {device}, buildid:{buildid}')
            title = self._find_page_title(search=f'{device} {buildid}')

        key_data = self._fetch_key_data(title=title)
        return self._parse_key_data(data=key_data)
