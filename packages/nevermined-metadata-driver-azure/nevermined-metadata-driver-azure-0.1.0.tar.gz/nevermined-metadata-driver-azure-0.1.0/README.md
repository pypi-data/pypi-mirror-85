[![banner](https://raw.githubusercontent.com/nevermined-io/assets/main/images/logo/banner_logo.png)](https://nevermined.io)

# Metadata Azure Driver

> 💧 Metadata Azure Data Driver Implementation
> [nevermined.io](https://nevermined.io)

[![PyPI](https://img.shields.io/pypi/v/nevermined-metadata-azure-driver.svg)](https://pypi.org/project/nevermined-metadata-azure-driver/)
[![Python package](https://github.com/nevermined-io/metadata-azure-driver/workflows/Python%20package/badge.svg)](https://github.com/nevermined-io/metadata-azure-driver/actions)

---
## Table of Contents

  - [Quickstart](#quickstart)
  - [Code style](#code-style)
  - [Testing](#testing)
  - [New Version](#new-version)
  - [License](#license)

---

## Quickstart

To login in Azure cloud you need to execute the driver with the next environment variables set:
```bash
AZURE_CLIENT_ID
AZURE_CLIENT_SECRET
AZURE_TENANT_ID
AZURE_SUBSCRIPTION_ID
```

To get information about how to create an App principal for Metadata Azure driver in your Azure account, please
refer to Azure documentation. Links:
  - [#1](https://docs.microsoft.com/en-us/python/azure/python-sdk-azure-authenticate?view=azure-python)
  - [#2](https://docs.microsoft.com/en-us/cli/azure/create-an-azure-service-principal-azure-cli?toc=%2Fazure%2Fazure-resource-manager%2Ftoc.json&view=azure-cli-latest)
  - [#3](https://docs.microsoft.com/en-us/azure/azure-resource-manager/resource-group-create-service-principal-portal)


At the moment there is only a first implementation for the data_plugin, but in the future is going to be an instance 
for the computing plugin as well.

    
## Testing

Automatic tests are setup via Travis, executing `tox`.
Our test use pytest framework.

## New Version

The `bumpversion.sh` script helps to bump the project version. You can execute the script using as first argument {major|minor|patch} to bump accordingly the version.

## Attribution

This project is based in the Ocean Protocol [osmosis-azure-driver](https://github.com/oceanprotocol/osmosis-azure-driver).
It keeps the same Apache v2 License and adds some improvements. See [NOTICE file](NOTICE).

## License

```
Copyright 2020 Keyko GmbH
This product includes software developed at
BigchainDB GmbH and Ocean Protocol (https://www.oceanprotocol.com/)

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```