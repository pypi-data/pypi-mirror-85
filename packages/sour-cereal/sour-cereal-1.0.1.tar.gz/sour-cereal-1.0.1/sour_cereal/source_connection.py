from typing import Any

from .base.source_connection_interface import SourceConnectionInterface
from .base.extraction import Extraction


class SourceConnection(SourceConnectionInterface):
    '''Abstract class for a basic data source connection.

    It implements a base interface and adds a new method for creating extrac-
    tions.

    This class was written alongside and using a base interface for modularity
    purposes.
    '''
    def new_extraction(
        self: 'SourceConnection',
        parameters: Any = None
    ) -> Extraction:
        '''Return a new extraction with parameters and this instance as source.
        '''
        return Extraction(source=self, parameters=parameters)
