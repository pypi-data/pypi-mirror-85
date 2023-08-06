# Monte Carlo CLI
Monte Carlo's Alpha CLI!

## Installation
Requires Python 3.7 or greater. Normally you can install and update using pip. For instance: 
```
virtualenv venv
. venv/bin/activate

pip install -U montecarlodata
```
Developers of the CLI can use:
```
make install 
. venv/bin/activate
```

Either way confirm the installation by running:
```
montecarlo --version
```

If the Python requirement does not work for you please reach out to `customer-success@montecarlodata.com`. Docker is an option.

## Quick start
First time users can configure the tool by following the onscreen prompts:
```
montecarlo configure
```
MCD tokens can be generated from the [dashboard](https://getmontecarlo.com/).
 
Any AWS profiles or regions should be for the account the Data Collector (DC) is deployed to.

Use the `--help` flag for details on any advanced options (e.g. creating multiple montecarlo profiles) or any prompts.

That's it! You can always validate your connection with:
```
montecarlo validate
```

## User settings
Any configuration set by `montecarlo configure` can be found in '~/.mcd/' by default.

The MCD ID and Token can be overwritten, or even set, by the environment:
- MCD_DEFAULT_API_ID
- MCD_DEFAULT_API_TOKEN

These two are required either as part of `configure` or as environment variables. 
For AWS, system defaults are used if not set as part of `configure`

The following values can also be set by the environment:
- MCD_API_ENDPOINT - Overwrite the default API endpoint
- MCD_VERBOSE_ERRORS - Enable verbose logging on errors (default=false)

## Help
Documentation for commands, options and arguments can be found using the `--help` flag (per sub-command).

All commands, except `configure`, support an `--option-file` flag, which allows you to use a file in place of passing options. 
For instance, a `--name` flag can be set by creating a file containing:
```
name="Artemis"
```
Any dashes must be replaced by underscores. For instance, `--foo-bar` would be `foo_bar="qux"`.

Resolution is CLI Options > Option File.

## Examples
- Using Docker from a local installation
    ```
    docker build -t montecarlo .
    docker run -v ${HOME}/.aws/credentials:/root/.aws/credentials:ro \
               -e MCD_DEFAULT_API_ID='<ID>' \
               -e MCD_DEFAULT_API_TOKEN='<TOKEN>' \
               -e AWS_DEFAULT_PROFILE='<PROFILE>' \
               -e AWS_DEFAULT_REGION='us-east-1' \
               montecarlo --version
    ```
    Replace `--version` with any sub-commands or options. If interacting with files those directories will probably need to be mounted too.


- Configure a named profile with custom config-path
    ```
    $ montecarlo configure --profile-name odin --config-path .
    MCD ID: 1234
    MCD Token:  
    Repeat for confirmation: 
    AWS profile name []: thor
    AWS region [us-east-1]:
  
    $  cat ./profiles.ini 
    [odin]
    mcd_id = 1234
    mcd_token = 5678
    aws_profile = thor
    aws_region = us-east-1
    ```

- On-board `presto-sql` using an option-file and passing a certificate.
    ```
    $ montecarlo onboarding presto-sql --option-file ~/samples/sample_config --cert-file ~/samples/example_cert
    Uploaded '/Users/shiva/samples/example_cert' to s3://bucket/certificates/presto/example_cert
    Connection validated!
    Success! Added connection for Presto.
    ``` 
    Remember, an option-file can be used inplace of any options/args that would have been otherwise passed to the CLI.

## Tests and Releases
Locally, `make test` will run all tests. CircleCI manages all testing for deployment.

When ready to release make a PR for `master`. After merging CircleCI will test and deploy to [PyPI](https://pypi.org/project/montecarlodata/).

Don't forget to increment the version number in `setup.py` first! An existing version will not be deployed.

## License
Apache 2.0 - See the [LICENSE](http://www.apache.org/licenses/LICENSE-2.0) for more information.