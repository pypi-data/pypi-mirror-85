# VGS CLI
[![CircleCI](https://circleci.com/gh/verygoodsecurity/vgs-cli/tree/master.svg?style=svg&circle-token=dff66120c964e4fbf51dcf059b03746910d0449d)](https://circleci.com/gh/verygoodsecurity/vgs-cli/tree/master)

Command Line Tool for programmatic configurations on VGS.

[Official Documentation](https://www.verygoodsecurity.com/docs/vgs-cli/getting-started)

## Table of Contents

- [Requirements](#requirements)
- [Installation](#installation)
  - [PyPI](#pypi)
- [Run](#run)
- [Running in Docker](#running-in-docker)
- [Commands](#commands)
    
## Requirements
[Python 3](https://www.python.org/downloads/) or [Docker](https://docs.docker.com/get-docker/).

## Installation

### PyPI
Install the latest version from [PyPI](https://pypi.org/project/vgs-cli/):
```
pip install vgs-cli
```

## Run

Verify your installation by running:
```
vgs --version
```

## Running in Docker

In order to run in Docker we recommend to declare the following `docker-compose.yaml`:
```yaml
version: '3'
services:

  cli:
    image: quay.io/verygoodsecurity/vgs-cli:${VERSION:-latest}
    env_file:
      - .env
    ports:
      - "7745:7745"
      - "8390:8390"
      - "9056:9056"
    volumes:
      - ./.tmp:/tmp
```

To login from browser you need to pass `--service-ports` option:
```
docker-compose run --service-ports cli vgs login
```

To use auto login option you need to declare the following `.env` file:
```
VGS_CLIENT_ID=<YOUR-CLIENT-ID>
VGS_CLIENT_SECRET=<YOUR-CLIENT-SECRET>
``` 

Run the latest version with:
```
docker-compose run cli vgs --version
```

Run a specific version:
```
VERSION=[VERSION] docker-compose run cli vgs --version
``` 
## Commands

- [`help`](https://www.verygoodsecurity.com/docs/vgs-cli/commands#exploring-the-cli)
- [`login`](https://www.verygoodsecurity.com/docs/vgs-cli/commands#login) and [auto login](https://www.verygoodsecurity.com/docs/vgs-cli/commands#auto-login)  
- [`logout`](https://www.verygoodsecurity.com/docs/vgs-cli/commands#logout)
- [`routes get`](https://www.verygoodsecurity.com/docs/vgs-cli/commands#get)
- [`routes apply`](https://www.verygoodsecurity.com/docs/vgs-cli/commands#apply)
- [`logs access`](https://www.verygoodsecurity.com/docs/vgs-cli/commands#access)

## Sphinx Documentation

In order to generate [Sphinx](https://www.sphinx-doc.org/en/master/index.html) documentation:
```
pip install -r dev-requirements.txt
cd docs
make html
```
Check the generated docs:
```
open build/html/index.html
```

## Plugins Development

See [Click - Developing Plugins](https://github.com/click-contrib/click-plugins#developing-plugins).

In order to develop a plugin you need to register your commands to an entrypoint in `setup.py`.

Supported entrypoints:

- `vgs.plugins` - for extending `vgs` with sub-commands
- `vgs.get.plugins` - for extending `vgs get` with sub-commands
- `vgs.apply.plugins` - for extending `vgs apply` with sub-commands
- `vgs.logs.plugins` - for extending `vgs logs` with sub-commands

Example:
```python
entry_points='''
    [vgs.plugins]
    activate=vgscliadmin.admin:activate
    
    [vgs.get.plugins]
    preferences=vgscliadmin.admin:get_preferences
'''
```
