## Cleaner

##### A tool that cleans after you

Comments out or deletes code between tags.
Especially useful when you are doing a lot of changes for debugging (setting traces, printing some stuff etc.)
in big codebase within many files.
So after all you no need to worry about removing redundant code.

### Installation
* `git clone https://github.com/Symonen/cleaner`
* `ln -s <path_to_cleaner> /usr/bin/clean`
* I suggest to create live template in pycharm that wraps your code into a tags very convinient

And then you can just type `clean` in your project dir.


### Example
How it works:
* Iterates recursively over files in specified path.
* Deleting or commenting out code between tags
