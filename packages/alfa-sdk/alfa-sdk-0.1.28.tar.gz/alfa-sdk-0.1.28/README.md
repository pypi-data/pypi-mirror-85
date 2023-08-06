# alfa-sdk

This package provides a Python SDK for developing algorithms using [ALFA](https://widgetbrain.com/product/).

## Installation

You can directly install alfa-sdk using [pip](http://www.pip-installer.org/en/latest/). This will install the alfa-sdk package as well as all dependencies.

```sh
$ pip install alfa-sdk
```

If you already have alfa-sdk installed and want to upgrade to the latest version, you can run:

```sh
$ pip install --upgrade alfa-sdk
```

## Development

To install requirements locally:

**1.** Activate local venv

```sh
$ virtualenv venv
$ source venv/bin/activate
```

**2.** Install requirements from setup.py

```sh
$ pip install -e .[dev]
```

## Changelog
- 0.1.28 (2020-11-13)
  - Added support for macaroon tokens specified in ALFA_CONTEXT to authenticate requests
- 0.1.26 (2020-10-9)
  - Added function argument to IntegrationClient.invoke and definition of function_type
- 0.1.25 (2020-9-29)
  - Added support for integrations
- 0.1.21 (?)
  - fetch data for Meta Unit from Alfa when it exists
- 0.1.20 (2020-3-24)
  - enabled fetching secret values of a team the client is allowed to access
- 0.1.19 (2020-3-12)
  - enabled the definition of the team_id of a client
- 0.1.18 (2020-3-9)
  - added Dataclient.update_data_file method
- 0.1.17 (2020-3-5)
  - added fallback mechanisms for local handling of MetaInstances when there is no file found locally
- 0.1.16 (2020-3-4)
  - added AlgorithmClient.get_context
  - added AlgorithmClient.get_active_instance_from_context
  - added local handling of MetaUnits and MetaInstances
- 0.1.15 (2020-2-19)
  - added prefix, skip, limit, and order arguments to list_data_files function
- 0.1.14 (2020-1-27)
  - replace deprecated secrets service
- 0.1.13 (2020-1-22)
  - add store_kpi function
- 0.1.12 (2020-1-09)
  - generalize errors according to alfa errors
  - handle errors based on error codes
- 0.1.11 (2019-9-02)
  - generalized auth tokens
- 0.1.10 (2019-7-15)
  - allow handling of instances without storing to disk
- 0.1.0 - 0.1.9 (2019-3-19)
  - initial version + bugfixes
