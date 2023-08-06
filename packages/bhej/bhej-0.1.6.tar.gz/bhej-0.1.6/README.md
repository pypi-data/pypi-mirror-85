# bhej

> Share files like a dev.

## Installation

To install this cli to your environment, just run...

```[bash]
pip install bhej
```

...and you're good to go!

## Usages

To upload a file, just run the following.

```[bash]
bhej up <filename>
# You'll receive a 6 digit code to share.
# You'll also get a link that you can directly download from.
```

To download a file, just run the following.

```[bash]
bhej down <code> # Use the 6 digit code from the upload step.
```

## Development

Want to contribute? After cloning and `cd`-ing into the project directory,
you can run the following to get set up.

```[bash]
poetry shell    # Sets up virtual environment.
poetry install  # Installs dependencies.
which bhej      # Should return your local version of the CLI.
```

### Deploying to PyPi

To deploy to Test PyPi, run `poetry run deploy_staging`. To deploy to the Prod PyPi, run `poetry run deploy_prod`.

To install it from Test PyPi, run the following.

```[bash]
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple bhej
```

To install from Prod PyPi, run `pip install bhej`.
