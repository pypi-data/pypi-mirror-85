[![banner](https://raw.githubusercontent.com/nevermined-io/assets/main/images/logo/banner_logo.png)](https://nevermined.io)

# metadata-driver-aws

> Metadata AWS Data Driver Implementation
> [nevermined.io](https://nevermined.io)


[![PyPI](https://img.shields.io/pypi/v/nevermined-metadata-driver-aws.svg)](https://pypi.org/project/nevermined-metadata-driver-aws/)
[![Python package](https://github.com/nevermined-io/metadata-driver-aws/workflows/Python%20package/badge.svg)](https://github.com/nevermined-io/metadata-driver-aws/actions)


---

## Table of Contents

- [Setup](#setup)
- [Code Style](#code-style)
- [Testing](#testing)
- [New Version](#new-version)
- [License](#license)

---

## Setup

To use Amazon S3 storage with the gateway, you must set up some Amazon S3 storage and set some AWS configuration settings on the computer where Brizo is running. For details, see:

## Testing

Automatic tests are setup via Github actions.
Our tests use the pytest framework.

## New Version

The `bumpversion.sh` script helps to bump the project version. You can execute the script using as first argument {major|minor|patch} to bump accordingly the version.

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

Note: Installing this package (metadata-driver-aws) installs the boto3 package which also has an Apache-2.0 license. Installing boto3 installs the docutils package. The docutils package might have licensing that is incompatible with the Apache-2.0 license. We have opened [an issue](https://github.com/boto/boto3/issues/1916) on the boto3 repository to let them know about the potential licensing conflict and to resolve it if necessary.
