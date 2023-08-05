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

from typing import Dict, Any, Iterable

from pywaclient.endpoints import Endpoint


class WorldEndpoint(Endpoint):

    def __init__(self, client: 'AragornApiClient'):
        super().__init__(client)
        self.path = 'world/{0}'
        self.path_articles = 'world/{0}/articles'
        self.path_blocks = 'world/{0}/blocks'
        self.path_images = 'world/{0}/images'

    def get(self, identifier: str) -> Dict:
        """Get the metadata of a specific world.

        :param identifier: Identifier of the world.
        :return: World metadata.
        """
        return self._request(self.path.format(identifier))

    def articles(self, identifier: str, **kwargs) -> Iterable[Dict[str, Any]]:
        """Retrieve all the article metadata from a world.

        :param identifier: Identifier of the world.
        :keyword term: A string to query in the data. Will exclude any articles which do not contain this
                        term. Searches the following fields: title, tags, vignette content, sidebar elements,
                        footer and notes.
        :keyword order_by: The field the articles should be ordered by. Allowed values:
                            id (DEFAULT) | title | notification_date | creation_date
        :keyword trajectory: ASC (DEFAULT) | DESC
        :return: Iterator over article metadata.
        """
        for key in kwargs:
            assert key in ['term', 'order_by', 'trajectory']
            if key == 'order_by':
                assert kwargs[key] in ['id', 'title', 'notification_date', 'creation_date']
            if key == 'trajectory':
                assert kwargs[key] in ['ASC', 'DESC']
        return self._scroll_collection(self.path_articles.format(identifier), 'articles', **kwargs)

    def blocks(self, identifier: str, **kwargs) -> Iterable[Dict[str, Any]]:
        """Retrieve all the block metadata from a world.

        :param identifier: Identifier of the world.
        :keyword order_by: The field the blocks should be ordered by. Allowed values:
                            id (DEFAULT) | title
        :keyword trajectory: ASC (DEFAULT) | DESC
        :return: Iterator over block metadata.
        """
        for key in kwargs:
            assert key in ['order_by', 'trajectory']
            if key == 'order_by':
                assert kwargs[key] in ['id', 'title']
            if key == 'trajectory':
                assert kwargs[key] in ['ASC', 'DESC']
        return self._scroll_collection(self.path_blocks.format(identifier), 'blocks', **kwargs)

    def images(self, identifier: str, **kwargs) -> Iterable[Dict[str, Any]]:
        """Retrieve all the image metadata from a world.

        :param identifier: Identifier of the world.
        :keyword order_by: The field the images should be ordered by. Allowed values:
                            id (DEFAULT) | title
        :keyword trajectory: ASC (DEFAULT) | DESC
        :return: Iterator over image metadata.
        """
        for key in kwargs:
            assert key in ['order_by', 'trajectory']
            if key == 'order_by':
                assert kwargs[key] in ['id', 'title']
            if key == 'trajectory':
                assert kwargs[key] in ['ASC', 'DESC']
        return self._scroll_collection(self.path_images.format(identifier), 'images', **kwargs)
