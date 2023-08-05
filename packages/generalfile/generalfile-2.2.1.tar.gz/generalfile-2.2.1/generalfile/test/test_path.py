
import unittest

from generalfile import Path
from generalfile.test.setup_workdir import setup_workdir
from generalfile.errors import InvalidCharacterError


class PathTest(unittest.TestCase):
    def setUp(self):
        """Set working dir and clear folder. Set path delimiter to '/' for testing."""
        Path.path_delimiter = "/"
        setup_workdir()


class FileTest(PathTest):
    def test_path(self):
        self.assertRaises(InvalidCharacterError, Path, "hello:there")
        self.assertRaises(InvalidCharacterError, Path, "hello<")
        self.assertRaises(InvalidCharacterError, Path, "hello>")
        self.assertRaises(InvalidCharacterError, Path, "hello.")

    def test_addPath(self):
        self.assertEqual(Path("foo/bar"), Path("foo") / "bar")
        self.assertEqual(Path("foo/bar"), Path("foo") / Path("bar"))
        self.assertEqual(Path("foo.txt/folder"), Path("foo.txt") / "folder")
        self.assertEqual(Path("folder/foo.txt"), Path("folder") / "foo.txt")

    def test_parts(self):
        path = Path("folder/folder2/test.txt")
        self.assertEqual(["folder", "folder2", "test.txt"], path.parts())

    def test_name(self):
        path = Path("folder/test.txt")
        self.assertEqual("test.txt", path.name())

        self.assertEqual("folder/foobar.txt", path.with_name("foobar.txt"))
        self.assertEqual("folder/hi", path.with_name("hi"))

    def test_stem(self):
        path = Path("folder/test.txt")
        self.assertEqual("test", path.stem())
        self.assertEqual("folder/foobar.txt", path.with_stem("foobar"))

        path = Path("folder/test.foo.txt.bar")
        self.assertEqual("test.foo.txt", path.stem())
        self.assertEqual("folder/foo.bar", path.with_stem("foo"))

    def test_true_stem(self):
        path = Path("folder/test.txt")
        self.assertEqual("test", path.true_stem())
        self.assertEqual("folder/foobar.txt", path.with_true_stem("foobar"))

        path = Path("folder/test.foo.txt.bar")
        self.assertEqual("test", path.true_stem())
        self.assertEqual("folder/yo.foo.txt.bar", path.with_true_stem("yo"))

    def test_suffixes(self):
        path = Path("folder/test.hello.txt")
        self.assertEqual([".hello", ".txt"], path.suffixes())
        self.assertEqual("folder/test.tsv", path.with_suffixes([".tsv"]))

    def test_suffix(self):
        path = Path("folder/test.txt")
        self.assertEqual(".txt", path.suffix())

        path = path.with_suffix(".tsv")
        self.assertEqual("folder/test.tsv", path)

        path = path.with_suffix(".csv")
        self.assertEqual("folder/test.csv", path)

        path = path.with_suffix(".BACKUP", -2)
        self.assertEqual("folder/test.BACKUP.csv", path)

        path = path.with_suffix(".test", -2)
        self.assertEqual("folder/test.test.csv", path)

        path = path.with_suffix(None, 0)
        self.assertEqual("folder/test.csv", path)

        path = path.with_suffix(".foo", 2)
        self.assertEqual("folder/test.csv.foo", path)

        path = path.with_suffix(".bar", 3)
        self.assertEqual("folder/test.csv.foo.bar", path)

        path = path.with_suffix(".clamped", 5)
        self.assertEqual("folder/test.csv.foo.bar.clamped", path)

        path = path.with_suffix(".clamped", -10)
        self.assertEqual("folder/test.clamped.csv.foo.bar.clamped", path)

        path = path.with_suffix(None, 10)
        self.assertEqual("folder/test.clamped.csv.foo.bar", path)

        path = path.with_suffix(None, -10)
        self.assertEqual("folder/test.csv.foo.bar", path)

    def test_parent(self):
        path = Path("folder/foobar/test.txt")
        self.assertEqual(Path("folder/foobar"), path.parent())
        self.assertEqual(Path("folder/foobar"), path.parent(0))
        self.assertEqual(Path("folder"), path.parent(1))
        self.assertEqual(Path(), path.parent(2))
        self.assertRaises(Exception, path.parent, 3)

    def test_startswith(self):
        self.assertFalse(Path("file.txt").startswith("folder"))
        self.assertTrue(Path("file.txt").startswith("file"))
        self.assertFalse(Path("folder/file.txt").startswith("file.txt"))
        self.assertFalse(Path("folder/file.txt").absolute().startswith("folder"))

        self.assertTrue(Path("folder/file.txt").startswith("folder"))
        self.assertTrue(Path("file.txt").startswith("file.txt"))
        self.assertTrue(Path("file.SUFFIX.txt").startswith("file.SUFFIX.txt"))
        self.assertFalse(Path("filE.txt").startswith("file.txt"))

    def test_endswith(self):
        self.assertFalse(Path("file.txt").endswith("folder"))
        self.assertFalse(Path("file.txt").endswith("file"))
        self.assertFalse(Path("folder/file.txt").endswith("folder"))
        self.assertFalse(Path("folder/file.txt").absolute().endswith("file"))

        self.assertTrue(Path("folder/file.txt").endswith("file.txt"))
        self.assertTrue(Path("folder/file.txt").endswith("txt"))
        self.assertTrue(Path("file.txt").endswith("file.txt"))
        self.assertFalse(Path("filE.txt").endswith("file.txt"))

    def test_remove_start(self):
        self.assertEqual(Path(), Path("test.txt").remove_start("test.txt"))
        self.assertEqual(Path("folder/test.txt"), Path("folder/test.txt").remove_start("Folder"))
        self.assertEqual(Path("test.txt"), Path("folder/test.txt").remove_start("folder"))
        self.assertEqual(Path("folder/test.txt"), Path("folder/test.txt").remove_start("test"))

        if Path.verInfo.pathRootIsDelimiter:
            self.assertEqual(Path("test.txt"), Path("folder/test.txt").remove_start("folder"))

    def test_remove_end(self):
        self.assertEqual(Path(), Path("test.txt").remove_end("test.txt"))
        self.assertEqual(Path("test"), Path("test.txt").remove_end(".txt"), "test")
        self.assertEqual(Path("folder"), Path("folder/test.txt").remove_end("test.txt"))
        self.assertEqual(Path("folder/test.txt"), Path("folder/test.txt").remove_end("test"))

    def test_absolute(self):
        path = Path("test.txt")
        self.assertEqual(False, path.is_absolute())
        self.assertEqual(True, path.is_relative())

        path = path.absolute()
        self.assertEqual(True, path.is_absolute())
        self.assertEqual(False, path.is_relative())

        path = path.relative()
        self.assertEqual(False, path.is_absolute())
        self.assertEqual(True, path.is_relative())


        path = Path("folder/folder2/file.txt")
        self.assertEqual(Path("folder2/file.txt"), path.relative("folder"))
        self.assertEqual(path.relative("folder"), "folder2/file.txt")
        self.assertEqual(path.relative("folder/folder2"), "file.txt")



    def test_is_file_or_folder(self):
        Path("folder.txt/file.txt").write()
        self.assertEqual(True, Path("folder.txt").is_folder())
        self.assertEqual(False, Path("folder.txt").is_file())

        self.assertEqual(True, Path("folder.txt/file.txt").is_file())
        self.assertEqual(False, Path("folder.txt/file.txt").is_folder())

    def test_exists(self):
        path = Path("folder/test.txt")
        self.assertEqual(False, path.exists())
        self.assertEqual(False, Path("folder").exists())

        path.write()
        self.assertEqual(True, path.exists())
        self.assertEqual(True, Path("folder").exists())
        self.assertEqual(False, Path("folder/test").exists())

        Path("folder").delete()
        self.assertEqual(False, path.exists())
        self.assertEqual(False, Path("folder").exists())


    def test_working_dir(self):
        self.assertEqual(True, Path.get_working_dir().is_absolute())
        self.assertEqual(Path().absolute(), Path.get_working_dir())

        Path("folder").set_working_dir()
        self.assertEqual(True, Path.get_working_dir().endswith("folder"))
        self.assertEqual(Path().absolute(), Path.get_working_dir())

    def test_same_destination(self):
        path = Path("folder")
        self.assertEqual(True, path.same_destination(Path() / "folder"))
        self.assertEqual(True, path.same_destination(path.absolute()))
        self.assertEqual(True, path.same_destination("folder"))

    def test_write(self):
        self.assertEqual('"foobar"', Path("test.txt").write("foobar"))
        self.assertEqual("foobar", Path("test.txt").read())

        self.assertEqual('"foobar"', Path("test2").write("foobar"))
        self.assertEqual("foobar", Path("test2").read())

        self.assertEqual('"foobar"', Path("test2.doesntexist").write("foobar"))
        self.assertEqual("foobar", Path("test2.doesntexist").read())

        self.assertEqual('"foobar"', Path("folder/test.txt").write("foobar"))
        self.assertEqual("foobar", Path("folder/test.txt").read())

    def test_rename(self):
        Path("folder/test.txt").write()

        Path("folder/test.txt").rename(name="hello.txt")
        self.assertTrue(Path("folder/hello.txt").exists())
        self.assertFalse(Path("folder/test.txt").exists())

        Path("folder").rename(name="folder2")
        self.assertTrue(Path("folder2").exists())
        self.assertFalse(Path("folder").exists())

        Path("folder2/hello.txt").rename(name="foo.txt")
        self.assertTrue(Path("folder2/foo.txt").exists())

        Path("folder2/foo.txt").rename(name="foo.TEST.txt")
        self.assertTrue(Path("folder2/foo.TEST.txt").exists())

        Path("folder2/foo.TEST.txt").rename(name="foobar")
        self.assertTrue(Path("folder2/foobar").is_file())

        Path("folder2/foobar").rename(suffix=".test")
        self.assertTrue(Path("folder2/foobar.test").exists())

        Path("folder2/foobar.test").rename(stem="hello")
        self.assertTrue(Path("folder2/hello.test").exists())

    def test_copy(self):
        Path("folder/test.txt").write()
        Path("folder/test.txt").copy("foo.txt")
        self.assertEqual(True, Path("folder/foo.txt").exists())

        Path("folder").copy("new")
        self.assertEqual(True, Path("new/foo.txt").exists())

        Path("new/foo.txt").copy("new/bar.txt")
        self.assertEqual(True, Path("new/bar.txt").exists())

    def test_copy_to_folder(self):
        Path("folder/test.txt").write()
        Path("folder/test2.txt").write()

        Path("folder").copy_to_folder("folder2")
        self.assertEqual(True, Path("folder2/test.txt").exists())
        self.assertEqual(True, Path("folder2/test2.txt").exists())
        self.assertEqual(True, Path("folder/test2.txt").exists())

        Path("folder/test.txt").copy_to_folder("")
        self.assertEqual(True, Path("test.txt").exists())
        self.assertEqual(False, Path("test2.txt").exists())

        Path("folder").copy_to_folder(Path(), overwrite=True)
        self.assertEqual(True, Path("test2.txt").exists())

    def test_move(self):
        Path("folder/test.txt").write(5)
        Path("folder/test2.txt").write()

        Path("folder").move("folder2")
        self.assertEqual(False, Path("folder").exists())
        self.assertEqual(True, Path("folder2/test.txt").exists())
        self.assertEqual(True, Path("folder2/test2.txt").exists())

        Path("folder2/test.txt").move("")
        self.assertEqual(True, Path("test.txt").exists())
        self.assertEqual(False, Path("test2.txt").exists())
        self.assertEqual(False, Path("folder2/test.txt").exists())

        Path("folder/test.txt").write(2)
        with self.assertRaises(FileExistsError):
            Path("folder").move(Path())

        self.assertEqual(5, Path("test.txt").read())
        Path("folder").move(Path(), overwrite=True)
        self.assertEqual(2, Path("test.txt").read())

    def test_create_folder(self):
        path = Path("folder/folder2.txt")
        path.create_folder()

        self.assertEqual(True, path.is_folder())

    def test_trash_and_delete(self):
        for method in ("trash", "delete"):
            path = Path("file.txt")
            self.assertEqual(False, path.exists())
            self.assertEqual(False, getattr(path, method)())

            path.write()
            self.assertEqual(True, path.exists())
            self.assertEqual(True, getattr(path, method)())
            self.assertEqual(False, getattr(path, method)())

            path = Path("folder/file.txt")
            self.assertEqual(False, path.exists())
            self.assertEqual(False, getattr(path, method)())

            path.write()
            self.assertEqual(True, path.exists())
            self.assertEqual(True, getattr(path.parent(), method)())
            self.assertEqual(False, getattr(path.parent(), method)())
            self.assertEqual(False, Path("folder").exists())

    def test_trash_and_delete_folder_content(self):
        for method in ("trash_folder_content", "delete_folder_content"):
            setup_workdir()

            mainPath = Path("folder")
            path = mainPath / "file.txt"
            path2 = mainPath / "folder2/file2.txt"
            self.assertEqual(False, mainPath.exists())
            self.assertEqual(False, getattr(mainPath, method)())

            for targetPath in (mainPath, ):
                path.write()
                path2.write()
                self.assertEqual(True, getattr(targetPath, method)())
                self.assertEqual(False, getattr(targetPath, method)())
                self.assertEqual(True, mainPath.exists())
                self.assertEqual(False, path.exists())
                self.assertEqual(False, path2.exists())

    def test_get_paths(self):
        Path("test.txt").write()
        Path("folder/test2.txt").write()
        Path("folder/test3.txt").write()

        self.assertEqual(2, len(list(Path().get_paths_recursive(depth=0))))
        self.assertEqual(3, len(list(Path().get_paths_recursive(depth=0, include_self=True))))

        self.assertEqual(1, len(list(Path("test.txt").get_paths_recursive(depth=0))))
        self.assertEqual(2, len(list(Path("test.txt").get_paths_recursive(depth=0, include_self=True))))

        self.assertEqual(4, len(list(Path().get_paths_recursive(depth=2))))
        self.assertEqual(5, len(list(Path().get_paths_recursive(depth=2, include_self=True))))
        self.assertEqual(5, len(list(Path().get_paths_recursive(depth=-1, include_self=True))))
        self.assertEqual(3, len(list(Path().get_paths_recursive(depth=0, include_self=True))))

        self.assertEqual(1, len(list(Path("folder/test2.txt").get_paths_recursive())))

    def test_time_created_and_modified(self):
        import time
        path = Path("test.txt")
        methods = (path.seconds_since_creation, path.seconds_since_modified)

        for method in methods:
            self.assertRaises(AttributeError, method)

        path.write()

        for method in methods:
            self.assertGreater(method(), 0)

        # Think you need to flush and stuff to make this work for windows atleast
        # self.assertEqual(methods[0](), methods[1]())
        # path.write("foobar", overwrite=True)
        # self.assertNotEqual(methods[0](), methods[1]())

    # def test_getitem(self):
    #     self.assertEqual("foo", Path("foo/bar")[0])
    #     self.assertEqual("bar", Path("foo/bar")[1])
    #
    #     self.assertEqual(not Path.verInfo.pathRootIsDelimiter, bool(Path().absolute()[0]))

    def test_threads(self):
        from generallibrary import sleep
        import multiprocessing as mp
        threads = []
        queue = mp.Queue()
        count = 2
        for i in range(count):
            threads.append(mp.Process(target=threadTest, args=(queue, i)))
        for thread in threads:
            thread.start()

        results = []
        for i in range(count):
            get = queue.get()
            self.assertNotIn(get, results)
            results.append(get)

        self.assertEqual(len(results), count)

def threadTest(queue, i):
    queue.put(int(Path("test.txt").write(i, overwrite=True)))

if __name__ == "__main__":
    x = unittest.main()












































