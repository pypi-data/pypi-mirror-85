# Ayarami
## Readme
### Introduction
Ayarami is a simple configuration manager, very similar to Django's settings system.
Main reasoning was, it was impossible to use django's settings without integrating django to the project.

### Setup
You can simply do `pip instal ayarami` or download the code and run `python setup.py install`.

## API
### How to use
Because this system is not tied to a project, and is a standalone solution, it does not come with a schema.
You are free to define your own schema and default values.

You can import the default settings object and call .configure() method to make it load a python file.
.configure() method takes a string to import or a module object.
It parses the file and loads the uppercase variables, variables starting with underscore will be ignored.

### Simple example

Let's say we have a default.py file 
```
import os
A = 10
_B = 20
C = os.getenv("PROJ_C", 30)
```

We can do this to load the file to default settings object:

```
from ayarami import settings
settings.configure("default.py")
# or
# import default as default_variables
# settings.configure(default_variables)
```

Another use case might be something such as this;

```
from ayarami import settings
import os
import default as default_variables
settings.configure(default_variables)
env_file = os.getenv("PROJ_SETTINGS_MODULE")
if env_file is not None:
    settings.configure(env_file)
else:
    raise ValueError("No PROJ_SETTINGS_MODULE environment variable defined")
```

Because of the nature of the library, you must configure settings before any call made to it, otherwise an error will 
be raised.
