
import pathlib


from generallibrary import VerInfo, initBases

from generalfile.errors import InvalidCharacterError
from generalfile.path_lock import Path_ContextManager
from generalfile.path_operations import Path_Operations
from generalfile.path_strings import Path_Strings
from generalfile.optional_dependencies.path_spreadsheet import Path_Spreadsheet
from generalfile.optional_dependencies.path_text import Path_Text


@initBases
class Path(Path_ContextManager, Path_Operations, Path_Strings, Path_Spreadsheet, Path_Text):
    """
    Immutable cross-platform Path.
    Wrapper for pathlib.
    Implements rules to ensure cross-platform compatability.
    Adds useful methods.
    """
    verInfo = VerInfo()
    path_delimiter = verInfo.pathDelimiter
    Path = ...

    def __init__(self, path=None):
        self._str_path = self._scrub(str_path="" if path is None else str(path))
        self._path = pathlib.Path(self._str_path)

    def __str__(self):
        return self._str_path

    def __repr__(self):
        return self.__str__()

    def __truediv__(self, other):
        return self.Path(self._path / str(other))

    def __eq__(self, other):
        return str(self) == str(other)

    def __hash__(self):
        return hash(str(self))

    def _scrub(self, str_path):
        str_path = self._replace_delimiters(str_path=str_path)
        str_path = self._invalid_characters(str_path=str_path)
        str_path = self._trim(str_path=str_path)
        return str_path

    def _replace_delimiters(self, str_path):
        str_path = str_path.replace("/", self.path_delimiter)
        str_path = str_path.replace("\\", self.path_delimiter)
        # str_path = str_path.replace(self.path_delimiter_alternative, self.path_delimiter)  # Don't remember why I commented this
        return str_path

    def _invalid_characters(self, str_path):
        # Simple invalid characters testing from Windows
        for character in '<>"|?*':
            if character in str_path:
                raise InvalidCharacterError(f"Invalid character '{character}' in '{str_path}'")
        if ":" in str_path:
            if not self.verInfo.pathRootHasColon:
                raise InvalidCharacterError(f"Path has a colon but '{self.verInfo.os}' doesn't use colon for path root: '{str_path}'")
            if str_path[1] != ":":
                raise InvalidCharacterError(f"Path has a colon but there's no colon at index 1: '{str_path}'")
            if len(str_path) >= 3 and str_path[2] != self.path_delimiter:
                raise InvalidCharacterError(f"Path has a colon but index 2 is not a delimiter: '{str_path}'")
            if ":" in str_path[2:]:
                raise InvalidCharacterError(f"Path has a colon that's not at index 1: '{str_path}'")
        if str_path.endswith("."):
            raise InvalidCharacterError(f"Path cannot end with a dot ('.').")
        return str_path

    def _trim(self, str_path):
        if not self.verInfo.pathRootIsDelimiter and str_path.startswith(self.path_delimiter):
            str_path = str_path[1:]
        if str_path.endswith(self.path_delimiter):
            str_path = str_path[0:-1]
        return str_path

setattr(Path, "Path", Path)















































