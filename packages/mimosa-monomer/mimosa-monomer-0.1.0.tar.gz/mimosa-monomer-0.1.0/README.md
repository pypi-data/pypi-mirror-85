# mimosa 
Database management CLI for **Stilt 2**.

## Installation
Run `pip install mimosa_monomer-0.0.1-py3-none-any.whl` to install the package
into your chosen python environment.

Be sure to update to the current wheel filename.

## Usage
Run `mimosa` in the terminal. Select the service account key file for the
desired Firebase project to connect to. Follow the prompts.

# Development
Run all tests with `tox` command.

Run tests and recreate virtual environments with `tox --recreate`.

## Docker Development Environment
You'll need Docker installed on your machine, obviously 😁.

### Clone This Repository
```
git clone https://github.com/hhelmric/mimosa.git
cd mimosa
```

### Build The Image

From cloned directory (where Dockerfile is located):
```
docker build . -t mimosa:latest
```

**If you have updated `pyproject.toml`, and are experiencing odd behavior, 
you may need to rebuild the image to get the correct dependencies.**

### Run The Container
From cloned directory.
```
docker-compose run app
```

This will run the container and begin a Bash terminal within. **The local source code directory will be synced with the container's `/code` directory.** Changes you make to source code in your IDE should be reflected in the container.

From here you can execute commands:

*  `tox` or `tox -e py38` to run tests against the installed version of the package.
*  `poetry add some_package` or `poetry add --dev some_package` to add dependencies to pyproject.toml.
*  `python -m mimosa.main` from within `src` folder to run the program against the non-installed source file.
*  `poetry build` builds the package for distribution.
*  `poetry publish` publishes package on pypi. You'll need a pypi account and to be added to the project as a collaborator.
