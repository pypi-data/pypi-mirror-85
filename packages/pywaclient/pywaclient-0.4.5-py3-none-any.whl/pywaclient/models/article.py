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
from typing import Dict, Any, List

from pywaclient.models.entity import Entity


class Article(Entity):

    def __init__(self, client: 'AragornApiClient', metadata: Dict[str, Any]):
        super().__init__(client, metadata)
        if 'full_render' in self._metadata:
            self._full_render = self._metadata['full_render']
            del self._metadata['full_render']
        else:
            self._full_render = ""

    @property
    def title(self) -> str:
        return self._metadata['title']

    @property
    def template(self) -> str:
        return self._metadata['template']

    @property
    def is_draft(self) -> bool:
        return self._metadata['is_draft']

    @property
    def is_wip(self) -> bool:
        return self._metadata['is_wip']

    @property
    def state(self) -> str:
        """State of the article: 'private' or 'public'."""
        return self._metadata['state']

    @property
    def wordcount(self) -> int:
        """Wordcount within the article."""
        return self._metadata['wordcount']

    @property
    def url(self) -> str:
        """Absolute url of the article."""
        return self._metadata['url']

    @property
    def tags(self) -> List[str]:
        """A list of all the tags on this article."""
        tags = self._metadata['tags']
        if tags is None:
            return list()
        else:
            return tags.split(',')

    @property
    def category(self) -> str:
        if 'category' in self._metadata:
            return self._metadata['category']['title']
        else:
            return 'NO_CATEGORY'

    @property
    def author_id(self) -> str:
        return self._metadata['author']['id']

    @property
    def author(self) -> 'User':
        from pywaclient.models.user import User
        return User(self._client, self._client.user.get(self.author_id))

    @property
    def world_id(self) -> str:
        return self._metadata['world']['id']

    @property
    def world(self) -> 'World':
        from pywaclient.models.world import World
        return World(self._client, self._client.world.get(self.world_id))

    @property
    def full_render(self) -> str:
        return self._full_render

    def to_json(self, indent='    ', ensure_ascii: bool = False, include_full_render: bool = False) -> str:
        if include_full_render:
            self._metadata['full_render'] = self._full_render
        return super().to_json(indent, ensure_ascii)
