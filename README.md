### Setup
We use a python virtual environment that modifies the python paths to use a pre-determined version and a local version of the python packages restricted to what is installed in the virtual environment. This is necessary for ensuring the requirements.txt is correct and greatly eases the deployment process.

There is a python virtual environment directory in the repository called venv. Before running the application any time, activate the virtual environment with: `$source venv/bin/activate`.

The first time before running the application, and whenever new dependencies are added to the requirements.txt, run $pip install -r requirements.txt AFTER activating the virtual environment.

### Running Locally
1. `$source venv/bin/activate`
2. `$python manage.py runserver`

This will start a development server on localhost at the port 8000.

### Deployment
Deployment is set up through Aaron's Heroku account. Let him know when there is a new version ready to be deployed.
