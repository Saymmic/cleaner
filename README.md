## Cleaner

##### A tool that cleans after you

Comments out or deletes code between tags.
Especially useful when you are doing a lot of changes for debugging (setting traces, printing some stuff etc.)
in big codebase within many files.

So after all you no need to worry about removing redundant code this script do this for you.

### Installation
* `git clone https://github.com/Symonen/cleaner`
* `ln -s <path_to_cleaner> /usr/bin/clean`
* I suggest to create live template in pycharm that wraps your code into a tags, very convenient.

And then you can just type `clean` in your project dir.


### How it works:
* Iterates recursively over files in specified path.
* Deleting or commenting out code between tags.

### Examples:

Lets suppose that in current directory we have file `example.py` with the following content:

```python
def bubble_sort(items):
    """ Implementation of bubble sort """
    for i in range(len(items)):
        for j in range(len(items) - 1 - i):
            if items[j] > items[j + 1]:
                items[j], items[j + 1] = items[j + 1], items[j]
```
but something is wrong and we want to do some debugging so we added debug lines and our file now looks like this:


```python
def bubble_sort(items):
    """ Implementation of bubble sort """
    print('DEBUG: START ALGORITHM')
    for i in range(len(items)):
        for j in range(len(items) - 1 - i):
            if items[j] > items[j + 1]:
                import pdb; pdb.set_trace()
                print(items[j])
                items[j], items[j + 1] = items[j + 1], items[j]
```

after fixing our problem we must clean up code and make sure that all of redundant code was removed. Sometimes we just want to
comment out the debug lines and then come back to them later. All of this is especially painful when we have a big codebase with
multiple files changed in different locations.

And thats why this little tool was created. It will clean up after you and will make sure that no redundant code remains.

So to use `cleaner` you need to wrap your code into tags which is very simple using your custom live template (in jet brains products) 
The file should look like this now:

```python
def bubble_sort(items):
    """ Implementation of bubble sort """
    # ▼▼▼ MY TEMP CODE. DELETE ME ▼▼▼
    print('DEBUG: START ALGORITHM')
    # ▲▲▲ MY TEMP CODE. DELETE ME ▲▲▲
    for i in range(len(items)):
        for j in range(len(items) - 1 - i):
            if items[j] > items[j + 1]:
                # ▼▼▼ MY TEMP CODE. DELETE ME ▼▼▼
                import pdb; pdb.set_trace()
                print(items[j])
                # ▲▲▲ MY TEMP CODE. DELETE ME ▲▲▲
                items[j], items[j + 1] = items[j + 1], items[j]
```

After all we can use `cleaner` in the following way:    

`clean .` - will deletes tagged code from all your files in the current direcory and the file will look like this:
```python
def bubble_sort(items):
    """ Implementation of bubble sort """
    for i in range(len(items)):
        for j in range(len(items) - 1 - i):
            if items[j] > items[j + 1]:
                items[j], items[j + 1] = items[j + 1], items[j]
```

`clean . -c` - which will comment out the code and in result the file will look like this:
```python
def bubble_sort(items):
    """ Implementation of bubble sort """
    # ▼▼▼ MY TEMP CODE. DELETE ME ▼▼▼
#    print('DEBUG: START ALGORITHM')
    # ▲▲▲ MY TEMP CODE. DELETE ME ▲▲▲
    for i in range(len(items)):
        for j in range(len(items) - 1 - i):
            if items[j] > items[j + 1]:
                # ▼▼▼ MY TEMP CODE. DELETE ME ▼▼▼
#                import pdb; pdb.set_trace()
#                print(items[j])
                # ▲▲▲ MY TEMP CODE. DELETE ME ▲▲▲
                items[j], items[j + 1] = items[j + 1], items[j]
```

`clean . -u` - will reverse changes above uncommenting the code.
`clean . -d` - will just prints what files and lines will be affected. 


Wrapping tags, files and direcories to exclude can be easily changed in the `config.py` file.