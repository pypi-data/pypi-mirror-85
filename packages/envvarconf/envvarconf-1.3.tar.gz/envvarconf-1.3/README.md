# envvarconf
![Python application](https://github.com/a1fred/envvarconf/workflows/Python%20application/badge.svg?branch=master)

Safe app configuration from environment variables without extra dependencies

# Install
```
pip install envvarconf
```

# Example
Define our settings
```python3
from envvarconf import BaseSettings
from envvarconf.loaders import environ


class Settings(BaseSettings):
    SENTRY_DSN: str
    LOGGING_LEVEL: str = 'debug'

    HOST: str = "aaaakehgeiuhgiweurhiuerhf"*200
    PORT: int


if __name__ == "__main__":
    settings = Settings()
    settings.load(loader=environ.Loader())

    print("OK!")
    print(settings)
```

Run application without any environment definition
```bash
$ python3 main.py 
There is errors in settings
 * SENTRY_DSN is not defined
 * PORT is not defined

Application settings:
SENTRY_DSN: <class 'str'> = NOT DEFINED!
LOGGING_LEVEL: <class 'str'> = debug
HOST: <class 'str'> = aaaakehgeiuhgi...
PORT: <class 'int'> = NOT DEFINED!
```

Define HOST variable:
```bash
$ HOST=1 python3 main.py 
There is errors in settings
 * SENTRY_DSN is not defined
 * PORT is not defined

Application settings:
SENTRY_DSN: <class 'str'> = NOT DEFINED!
LOGGING_LEVEL: <class 'str'> = debug
HOST: <class 'str'> = 1
PORT: <class 'int'> = NOT DEFINED!

```

Define all variables
```bash
$ HOST=1 PORT=2 SENTRY_DSN=3 python3 main.py 
OK!
<Settings SENTRY_DSN=3, LOGGING_LEVEL=debug, HOST=1, PORT=2>
```
