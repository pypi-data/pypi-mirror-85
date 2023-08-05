

class Path_Strings:
    """ String operations for Path. """
    def __getitem__(self, item):
        """ Get character from path string.

            :param generalfile.Path self: """
        return self.Path(self._str_path.__getitem__(item))

    @property
    def get_part(self):
        """ Split path using it's delimiter. item=0 with an absolute path gives an empty string on a posix system.

            :param generalfile.Path self:
            :param i: Index of part"""
        return self._str_path.split(self.path_delimiter)

    def get_replaced_alternative_characters(self):
        """ Get a dictionary of all characters that are replaced for the alternative path.

            :param generalfile.Path self: """
        return {
            self.path_delimiter: "&#47;",
            ":": "&#58",
            ".": "&#46;"
        }

    def get_alternative_path(self):
        """ Get path using alternative delimiter and alternative root for windows.

            :param generalfile.Path self:
            :rtype: generalfile.Path """
        path = str(self.absolute())
        for char, alternative in self.get_replaced_alternative_characters().items():
            path = path.replace(char, alternative)
        return self.Path(path)

    def get_lock_path(self):
        """ Get absolute lock path pointing to actual lock.

            :param generalfile.Path self: """
        return self.get_lock_dir() / self.absolute().get_alternative_path()

    def get_path_from_alternative(self):
        """ Get path from an alternative representation with or without leading lock dir.

            :param generalfile.Path self:
            :rtype: generalfile.Path """

        path = str(self.remove_start(self.get_lock_dir()))
        for char, alternative in self.get_replaced_alternative_characters().items():
            path = path.replace(alternative, char)
        return self.Path(path)

    def absolute(self):
        """ Get new Path as absolute.

            :param generalfile.Path self:
            :rtype: generalfile.Path """
        if self.is_absolute():
            return self
        else:
            return self.get_working_dir() / self
            # return self.Path(self._path.absolute())

    def relative(self, base=None):
        """ Get new Path as relative.

            :param generalfile.Path self:
            :param base: Defaults to working dir. """
        if self.is_relative() and base is None:
            return self
        else:
            if base is None:
                base = self.get_working_dir()
            return self.Path() if self == base else self.Path(self._path.relative_to(str(base)))

    def is_absolute(self):
        """ Get whether this Path is absolute.

            :param generalfile.Path self: """
        return self._path.is_absolute()

    def is_relative(self):
        """ Get whether this Path is relative.

            :param generalfile.Path self: """
        return not self.is_absolute()

    def startswith(self, path):
        """ Get whether this Path starts with given string.

            :param generalfile.Path self:
            :param str or Path path:"""
        path = self.Path(path)
        return str(self).startswith(str(path))

    def endswith(self, path):
        """ Get whether this Path ends with given string.

            :param generalfile.Path self:
            :param str or Path path:"""
        path = self.Path(path)
        return str(self).endswith(str(path))

    def remove_start(self, path):
        """ Remove a string from the start of this Path.

            :param generalfile.Path self:
            :param str or Path path:"""
        path = self.Path(path)
        str_path = str(path)
        if not self.startswith(str_path):
            return self
        else:
            new_path = self.Path(str(self)[len(str_path):])
            if str(new_path).startswith(path.path_delimiter):
                return new_path[1:]
            else:
                return new_path

    def remove_end(self, path):
        """ Remove a string from the end of this Path.

            :param generalfile.Path self:
            :param str or Path path:"""
        path = self.Path(path)
        str_path = str(path)
        if not self.endswith(str_path):
            return self
        else:
            new_path = self.Path(str(self)[:-len(str_path)])
            if str(new_path).endswith(path.path_delimiter):
                return new_path[:-1]
            else:
                return new_path

    def same_destination(self, path):
        """ See if two paths point to the same destination.

            :param generalfile.Path self:
            :param str or Path path:"""
        path = self.Path(path)
        return self.absolute() == path.absolute()

    def parent(self, index=0):
        """ Get any parent as a new Path.
            Doesn't convert to absolute path even if needed.

            :param generalfile.Path self:
            :param index: Which parent, 0 is direct parent.
            :raises IndexError: If index doesn't exist.
            :rtype: generalfile.Path """
        strParent = str(self._path.parents[index])
        if strParent == ".":
            strParent = ""
        return self.Path(strParent)

    def parts(self):
        """ Split path using it's delimiter. With an absolute path the first index is an empty string on a posix system.

            :param generalfile.Path self: """
        return str(self).split(self.path_delimiter)

    def name(self):
        """ Get name of Path which is stem + suffix.

            :param generalfile.Path self: """
        return self._path.name

    def with_name(self, name):
        """ Get a new Path with new name which is stem + suffix.

            :param name: Name.
            :param generalfile.Path self:
            :rtype: generalfile.Path """
        return self.Path(self._path.with_name(str(name)))

    def stem(self):
        """ Get stem which is name without last suffix.

            :param generalfile.Path self: """
        return self._path.stem

    def with_stem(self, stem):
        """ Get a new Path with new stem which is name without last suffix.

            :param stem: New stem.
            :param generalfile.Path self:
            :rtype: generalfile.Path """
        return self.Path(self.with_name(f"{stem}{self.suffix()}"))

    def true_stem(self):
        """ Get true stem which is name without any suffixes.

            :param generalfile.Path self: """
        return self._path.stem.split(".")[0]

    def with_true_stem(self, true_stem):
        """ Get a new Path with new stem which is name without any suffixes.

            :param true_stem: New true stem.
            :param generalfile.Path self:
            :rtype: generalfile.Path """
        return self.Path(self.with_name(f"{true_stem}{''.join(self.suffixes())}"))

    def suffix(self):
        """ Get suffix which is name without stem.

            :param generalfile.Path self: """
        return self._path.suffix

    def with_suffix(self, suffix, index=-1):
        """ Get a new Path with a new suffix at any index.
            Index is automatically clamped if it's outside index range.
            Set suffix to `None` to remove a suffix.

            :param generalfile.Path self:
            :param suffix: New suffix, can be `None`.
            :param index: Suffix index to alter.
            :rtype: generalfile.Path """

        suffixes = self.suffixes()

        try:
            suffixes[index]
        except IndexError:
            if index >= len(suffixes):
                if suffix is None:
                    del suffixes[-1]
                else:
                    suffixes.append(suffix)
            else:
                if suffix is None:
                    del suffixes[0]
                else:
                    suffixes.insert(0, suffix)
        else:
            if suffix is None:
                del suffixes[index]
            else:
                suffixes[index] = suffix

        return self.with_name(f"{self.true_stem()}{''.join(suffixes)}")

    def suffixes(self):
        """ Get every suffix as a list.

            :param generalfile.Path self: """
        return self._path.suffixes

    def with_suffixes(self, suffixes):
        """ Get a new Path with a new list of suffixes.

            :param list or tuple suffixes: New list of suffixes.
            :param generalfile.Path self:
            :rtype: generalfile.Path """
        return self.Path(self.with_name(f"{self.true_stem()}{''.join(suffixes)}"))
