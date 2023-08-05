# Package: generalfile
File manager for intuitive cross-platform compatability with gathered useful functionality.
Generalfile operates on the middle ground of all relevant operating systems.
E.g. Windows being case insensitive -> Don't allow paths with same name but differeing case.

Uses a race condition safe lock mechanism for all file operations.

## Installation
```
pip install generalfile
```

## Features
| Module   | Name                  | Explanation                                                         |
|:---------|:----------------------|:--------------------------------------------------------------------|
| path     | Path                  | Immutable cross-platform Path.                                      |
| errors   | CaseSensitivityError  | Raised when an existing file matches a path but not the exact case. |
| errors   | InvalidCharacterError | Raised when using an invalid character.                             |

## Path
| Module          | Name                                | Explanation                                                                                     |
|:----------------|:------------------------------------|:------------------------------------------------------------------------------------------------|
| path_lock       | lock                                | Create a lock for this path unless path is inside `lock dir`.                                   |
| path_operations | copy                                | Copy a file or folder next to itself with a new name.                                           |
| path_operations | copy_to_folder                      | Copy file or files inside given folder to anything except it's own parent, use `copy` for that. |
| path_operations | create_folder                       | Create folder with this Path unless it exists                                                   |
| path_operations | delete                              | Delete a file or folder.                                                                        |
| path_operations | delete_folder_content               | Delete a file or folder and then create an empty folder in it's place.                          |
| path_operations | exists                              | Get whether this Path exists.                                                                   |
| path_operations | get_cache_dir                       | Get cache folder.                                                                               |
| path_operations | get_lock_dir                        | Get lock folder inside cache folder.                                                            |
| path_operations | get_paths_in_folder                 | Get a generator containing every child Path inside this folder, relative if possible.           |
| path_operations | get_paths_recursive                 | Get all paths that are next to this file or inside this folder.                                 |
| path_operations | get_working_dir                     | Get current working folder as a new Path.                                                       |
| path_operations | is_file                             | Get whether this Path is a file.                                                                |
| path_operations | is_folder                           | Get whether this Path is a folder.                                                              |
| path_operations | move                                | Move files inside given folder or file to anything except it's own parent.                      |
| path_operations | open_folder                         | Open folder to view it manually.                                                                |
| path_operations | read                                | Read this Path with JSON.                                                                       |
| path_operations | rename                              | Rename this single file or folder to anything.                                                  |
| path_operations | seconds_since_creation              | Get time in seconds since file was created.                                                     |
| path_operations | seconds_since_modified              | Get time in seconds since file was modified.                                                    |
| path_operations | set_working_dir                     | Set current working folder.                                                                     |
| path_operations | trash                               | Trash a file or folder.                                                                         |
| path_operations | trash_folder_content                | Trash a file or folder and then create an empty folder in it's place.                           |
| path_operations | without_file                        | Get this path without it's name if it's a file, otherwise it returns itself.                    |
| path_operations | write                               | Write to this Path with JSON.                                                                   |
| path_strings    | absolute                            | Get new Path as absolute.                                                                       |
| path_strings    | endswith                            | Get whether this Path ends with given string.                                                   |
| path_strings    | get_alternative_path                | Get path using alternative delimiter and alternative root for windows.                          |
| path_strings    | get_lock_path                       | Get absolute lock path pointing to actual lock.                                                 |
| path_strings    | get_path_from_alternative           | Get path from an alternative representation with or without leading lock dir.                   |
| path_strings    | get_replaced_alternative_characters | Get a dictionary of all characters that are replaced for the alternative path.                  |
| path_strings    | is_absolute                         | Get whether this Path is absolute.                                                              |
| path_strings    | is_relative                         | Get whether this Path is relative.                                                              |
| path_strings    | name                                | Get name of Path which is stem + suffix.                                                        |
| path_strings    | parent                              | Get any parent as a new Path.                                                                   |
| path_strings    | parts                               | Get list of parts building this Path as list of strings.                                        |
| path_strings    | relative                            | Get new Path as relative.                                                                       |
| path_strings    | remove_end                          | Remove a string from the end of this Path.                                                      |
| path_strings    | remove_start                        | Remove a string from the start of this Path.                                                    |
| path_strings    | same_destination                    | See if two paths point to the same destination.                                                 |
| path_strings    | startswith                          | Get whether this Path starts with given string.                                                 |
| path_strings    | stem                                | Get stem which is name without last suffix.                                                     |
| path_strings    | suffix                              | Get suffix which is name without stem.                                                          |
| path_strings    | suffixes                            | Get every suffix as a list.                                                                     |
| path_strings    | true_stem                           | Get true stem which is name without any suffixes.                                               |
| path_strings    | with_name                           | Get a new Path with new name which is stem + suffix.                                            |
| path_strings    | with_stem                           | Get a new Path with new stem which is name without last suffix.                                 |
| path_strings    | with_suffix                         | Get a new Path with a new suffix at any index.                                                  |
| path_strings    | with_suffixes                       | Get a new Path with a new list of suffixes.                                                     |
| path_strings    | with_true_stem                      | Get a new Path with new stem which is name without any suffixes.                                |

## Usage example
```python
from generalfile import Path

Path("newfolder/test.txt").write("foobar")  # Automatically creates new folder
assert Path("newfolder/test.txt").read() == "foobar"
Path("newfolder").delete()  # Delete entire folder

with Path("foo/bar.txt").lock():  # Recursively lock a file or even a folder which doesn't have to exist.
    pass  # The lock is created in a seperate cache folder, so you're free to do whatever you want in here
```

## TODO
 * Optional dependency: .npy for Numpy
 * Tell user to `pip install generalfile[spreadsheet]` instead of `requires pandas` - Probably update generallibrary