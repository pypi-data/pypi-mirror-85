![https://github.com/amirhm/mynb/actions?query=workflow%3AWindows](https://github.com/amirhm/mynb/workflows/Windows/badge.svg)

# Formating the jupyter notebooks
An small package to clear all the outputs of a jupyter notebooks. 

To use versioning on the notebooks, it is practical to clear the outputs of all cells (to only keep the code). 
The outputs are written in the same notebook file in binary format (base64) and are huge in size and not suitable to be versioned.  
This simple package adds a command to removes all the cell output (similar to invoking "Clear all outputs" from the jupyetr menu) and could be added on the pre-commit hooks. 



Jupyter itself has a command to do this, but not very reliable always
````
jupyter nbconvert --clear-outputs ...
````


## Install

````
pip install mynb
````
this will install the mynb as an standalone console application (CLI), where can be run from terminal.

````
>> mynb [filename] [options]

filename: filename or path to the ipynb, possible to use the wildcards
          to apply multiple notebooks (mynb *.ipynb) 
options:
  -h, --help     show this help message
  --inplace, -p  by default the command re-write the files, if this switch is use new file with "_cleared" suffix is created 
  --quite, -q    do not print anything  
````
