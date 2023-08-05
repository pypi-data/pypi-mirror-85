from typing import Dict, Any


class Genre:

    def __init__(self, metadata: Dict[str, Any]):
        self._metadata = metadata

    @property
    def id(self) -> str:
        """Id of the genre."""
        return self._metadata['id']

    @property
    def name(self) -> str:
        """Name of the genre."""
        return self._metadata['name']
