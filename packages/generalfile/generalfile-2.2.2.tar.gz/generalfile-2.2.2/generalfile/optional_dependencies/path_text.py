
from generallibrary import deco_cache, initBases

import re


class Path_Text:
    """ Text methods for Path. """
    @property
    @deco_cache()
    def text(self):
        """ Easy access to a dynamically one-time created Text class, initalized with self (Path). """
        return self._text()(self)

    @staticmethod
    @deco_cache()
    def _text():
        @initBases
        class _Text(_Extension):
            def write(self, text=None, overwrite=False):
                """ Write to this path with a given string. """
                with self.WriteContext(self.path, overwrite=overwrite) as write_path:
                    with open(str(write_path), "w") as file:
                        file.write(text)

            def read(self):
                """ Read from this path to get a string. """
                with self.ReadContext(self.path) as read_path:
                    with open(str(read_path), "r") as file:
                        return file.read()

            def append(self, string, newline=False):
                """ Append to this path with a given string. """
                with self.AppendContext(self.path) as append_path:
                    with open(str(append_path), "a") as file:
                        if newline:
                            file.write("\n")
                        file.write(string)

            def replace(self, d, regex=False):
                """ Replace matches in this path with a given dictionary. """
                with self.path.lock():
                    text = self.path.text.read()
                    for key, value in d.items():
                        if regex:
                            text = re.sub(key, value, text)
                        else:
                            text = text.replace(key, value)
                    self.path.text.write(text, overwrite=True)



        return _Text


from generalfile.path_operations import _Extension






































