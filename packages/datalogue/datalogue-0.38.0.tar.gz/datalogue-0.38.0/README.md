dtl-python-sdk
--------------

The Datalogue python SDK is an SDK to be able to interact with the platform from
code.

Full documentation is available [here](https://dtl-python-sdk.netlify.com)

## Installation

### Setting up pip configuration

Datalogue releases are deployed directly to PyPI, which means you don't need to change any local configurations to install a new release. However, because our versions are not static, we are not deploying releases to PyPI artifactory. The following steps will allow you to make a single configuration change that will allow you to download any Datalogue release.

In order to install release candidates, you will need to update your `~/.pip/pip.conf` file, to include the Test PyPI url as an external index. The contents of your `~/.pip/pip.conf` file should be as follows:

```
[install]
index-url = https://pypi.python.org/simple/
extra-index-url = https://testpypi.python.org/simple/
```

### Installing `datalogue` package

After setting up the pip configuration, installing `datalogue` package is not different than other python packages

```bash
pip3 install datalogue==<x.y.z>
```

Where `x.y.z` defines specific version of the `datalogue`. For instance, in order to install `0.30.0` you need to execute:

```bash
pip3 install datalogue==0.30.0
```

If you want to install the latest stable package, you can execute the following command. This command will ignore release candidates, packages in Test PyPI server, only install the latest package in PyPI.

```bash
pip3 install datalogue
```

### Use in requirements.txt file

```txt
datalogue==0.30.0
```

## Release Process

Normally releases have a designated branch i.e release-x.y.z. Changes and new functionality for the planned release will be merged to the designated release branch.

For your feature/fix branch to get merged to the target release branch, it will require to have an updated `release/notes.yaml` with a short description for the new feature or fix.

In the rare cases where your local branch needs to be released immediately, due to urgent fixes which are not part of a planned release, you will need to:
*  update `release/notes.yaml` with a short description of the work done
*  update `release/version.dtl` with the new sdk version.


## Environment Variables for Integration Tests
* `DTL_TEST_USERNAME`: Basically, an email address that is already signed up and has admin rights in its organization
* `DTL_TEST_PASSWORD`: Password for that corresponding user
* `DTL_TEST_URI`: Infrastructure to use for integration tests. It can be either locally deployed platform or remote platform such as internals

## SSL Verification

We dont have a way to ensure that our clients submit the right certificates, a workaround is to set the enviroment variable 
`DTL_SSL_VERIFY_CERT` to `false` in order to be able to create a valid session, be aware that this wont stop the warning messages.

## Sentry

`SENTRY_DSN` env variable should be set in the env where we deploy the SDK