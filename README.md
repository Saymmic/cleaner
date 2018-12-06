## Cleaner

##### A tool that cleans after you

TODO: Rewrite it

Have you ever programming in hurry adding tons of pdb set traces or some code that helps
you debug along with proper changes? After all you need to clean up unwanted code.
This tool will do that for you!

All you need to do is to import live templates to your pycharm arsenal and tag your `fast code`.
After all this scripts will delete or comments out code that is in between tags.

### Installation
TODO: Make it more clear and automatic

* `git clone https://github.com/Symonen/cleaner`
* `ln -s <path_to_cleaner> /usr/bin/clean`
* I suggest to create live template in pycharm that wraps your code into a tags

And then you can just type `clean`


### Example
TODO: Visulize it and give user proper example

How it works:
* Iterates recursively over files including only files that have required file extensions 
and excluding unwanted dirs
* Deleting or commenting out code between tags
