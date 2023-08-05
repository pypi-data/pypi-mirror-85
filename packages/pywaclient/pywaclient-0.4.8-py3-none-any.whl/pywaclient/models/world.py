#    Copyright 2020 Jonas Waeber
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
from typing import Optional, Dict, Iterable, List

from pywaclient.models.genre import Genre
from pywaclient.models.article import Article
from pywaclient.models.block import Block
from pywaclient.models.entity import Entity


class World(Entity):

    def __init__(self, client: 'AragornApiClient', metadata: Dict[str, str]):
        super().__init__(client, metadata)

    @property
    def name(self) -> str:
        """Get the name of the world"""
        return self._metadata['name']

    @property
    def url(self) -> str:
        """Absolute url to the worlds homepage."""
        return self._metadata['url']

    @property
    def display_css(self) -> Optional[str]:
        """Property to get the world CSS if present.

        :return: Returns the CSS or None
        """
        if 'display_css' in self._metadata and self._metadata['display_css']:
            return self._metadata['display_css']
        else:
            return None

    @property
    def locale(self) -> str:
        """The language setting of this world as code (e.g. en, de, es etc)."""
        return self._metadata['locale']

    @property
    def genres(self) -> List[Genre]:
        """The genres of this world."""
        if 'genres' in self._metadata:
            for genre in self._metadata['genres']:
                yield Genre(genre)
        else:
            return []

    def articles(self) -> Iterable[Article]:
        for article in self._client.world.articles(self.id):
            article = self._client.article.get(article['id'], return_error=False)
            if article is not None:
                yield Article(self._client, article)

    def blocks(self) -> Iterable[Block]:
        for block in self._client.world.blocks(self.id):
            block = self._client.block.get(block['id'], return_error=False)
            if block is not None:
                yield Block(self._client, block)
