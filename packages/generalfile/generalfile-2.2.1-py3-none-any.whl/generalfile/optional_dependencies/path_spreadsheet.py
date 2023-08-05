
from generallibrary import deco_cache, typeChecker, getRows, initBases


class Path_Spreadsheet:
    """ Spreadsheet methods for Path. """
    @property
    @deco_cache()
    def spreadsheet(self):
        """ Easy access to a dynamically one-time created Spreadsheet class, initalized with self (Path). """
        return self._spreadsheet()(self)

    @staticmethod
    @deco_cache()
    def _spreadsheet():
        @initBases
        class _Spreadsheet(_Extension):
            """ Contains all functionality to handle spreadsheet files.
                Such as CSV and TSV. """

            import pandas
            import csv

            pd, csv = pandas, csv

            def __init__(self, path):
                self.path = path

            def write(self, df=None, overwrite=False):
                """ Can write a bunch of different DataFrames to a TSV file.
                    Doesn't support advanced pandas functionality.
                    Should work with: Keys, Index and Transposed (8 combinations)
                    If DataFrame has both keys and index then cell A1 becomes NaN

                    TODO: Make it order columns if there are any so that they line up with append.

                    :param pandas.DataFrame df: Serializable by JSON
                    :param overwrite: Whether to allow overwriting or not. """

                typeChecker(df, self.pd.DataFrame)

                with self.WriteContext(self.path, overwrite=overwrite) as write_path:
                    if df.empty:
                        write_path.write()
                        return False, False

                    useHeader = self._indexIsNamed(df.columns)
                    useIndex = self._indexIsNamed(df.index)

                    df.to_csv(str(write_path), sep="\t", header=useHeader, index=useIndex)

                    return useHeader, useIndex

            def read(self, header=False, column=False):
                """
                If any cell becomes NaN then the header and column parameters are overriden silently.

                Can read a bunch of different DataFrames to a TSV file.
                Doesn't support advanced pandas functionality.
                Should work with: Keys, Index, Transposed, Header, Column (32 combinations).
                DataFrame in file can have a NaN A1 cell.

                :param bool header: Use headers or not, overriden if any top left cell is NaN
                :param bool column: Use columns or not, overriden if any top left cell is NaN
                :rtype: pd.DataFrame
                """

                header = "infer" if header else None
                column = 0 if column else None

                with self.ReadContext(self.path) as read_path:
                    try:
                        df = self._read_helper(read_path, header, column)
                    except self.pd.errors.EmptyDataError:
                        return self.pd.DataFrame()

                    # Get rid of empty cell (Happens if file was written with header=True, column=True)
                    headerFalseColumnFalse = self.pd.isna(df.iat[0, 0])
                    headerFalseColumnTrue = self.pd.isna(df.index[0])
                    headerTrueColumnFalse = str(df.columns[0]).startswith("Unnamed: ")
                    if headerFalseColumnFalse or headerFalseColumnTrue or headerTrueColumnFalse:
                        header = "infer"
                        column = 0
                        df = self._read_helper(read_path, header, column)
                    else:
                        # Get rid of name in index (Happens if file doesn't have an index and column=True)
                        # Doesn't happen other way around for some reason, guess it's the internal order in pandas
                        if df.index.name is not None:
                            if header is None and column == 0:
                                df.index.rename(None, inplace=True)
                            else:
                                header = None
                                column = None
                                df = self._read_helper(read_path, header, column)

                    if not self._indexIsNamed(df.columns):
                        df.columns = self.pd.RangeIndex(len(df.columns))
                    if not self._indexIsNamed(df.index):
                        df.index = self.pd.RangeIndex(len(df.index))

                    return df.convert_dtypes()

            def append(self, obj):
                """
                Append an obj containing lists or dicts to the end of a TSV file.
                If a dict is given and there are iterables as values then the keys of the dict are the first value in each row.
                Otherwise keys in dicts are ignored.

                Identical append objects
                 | [[1, 2, 3], [4, 5, 6]]
                 | [{"a": 1, "b": 2, "c": 3}, {"d": 4, "e": 5, "f": 6}]
                 | {1: {"b": 2, "c": 3}, 4: {"e": 5, "f": 6}}
                 | {1: [2, 3], 4: [5, 6]}

                # TODO: Should probably support DataFrame and Series as well

                :param obj: Iterable (Optionally inside another iterable) or a value for a single cell
                """
                with self.AppendContext(self.path) as append_path:
                    with open(str(append_path), "a") as file:
                        writer = self.csv.writer(file, delimiter = "\t", lineterminator = "\n")
                        for row in getRows(obj):
                            writer.writerow(row)


            def _indexIsNamed(self, index):
                """
                Simple version to see if a DataFrame index is named or not
                :param index: DataFrame's index (columns or index)
                """
                if str(index[0]) == "0" or str(index[0]) == "1":
                    return False
                else:
                    return True

            def _read_helper(self, path, header, column):
                return self.pd.read_csv(str(path), sep="\t", header=header, index_col=column).convert_dtypes()

            def _append_helper(self, iterable_obj, key=None):
                """
                Takes an object and returns a list of rows to use for appending.

                :param iterable_obj: Iterable
                :param key: If iterableObj had a key to assigned it it's given here
                :return: A
                """
                row = [key] if key else []
                if isinstance(iterable_obj, (list, tuple)):
                    row.extend(iterable_obj)
                elif isinstance(iterable_obj, dict):
                    for _, value in sorted(iterable_obj.items()):
                        row.append(value)
                return row

        return _Spreadsheet


from generalfile.path_operations import _Extension






































