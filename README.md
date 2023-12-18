### Install
This repo is an installable python app managed by [poetry](https://python-poetry.org/). To Install you have a few options:
* Clone the repo and run `poetry install` and then `poetry shell`. This is best for development.
* Run `pip install 'rsg_form_collector @ git+https://github.com/alexm-stfc/form-collector.git@main#egg=rsg_form_collector'`
* Add the above string as a dependency in another app.

Once you have it installed an the correct environment activated, you can invoke the app with `python -m rsg_form_collector`

### Setup
To get this to work, you need to create somee files in the working directory from which you will run the app.
* Create an allowed_respondents.json file. This is a simple JSON list of strings- email addresses who should be allowed to respond to the form.
* Create a config.toml file. At present only one key is required: `form_id`, a string which is the google form ID which you are interested in.
* Download a client_secret file from google, instructions here: [https://developers.google.com/forms/api/quickstart/python](https://developers.google.com/forms/api/quickstart/python) . The file you dowload will have a long name, you need to rename it client_secret.json. NB: A credentials.json file is note required. It is created by the Oauth2 flow when you first run the app.

### Inital run
The first time you run the app, it will open a webserver to redirect you to the oauth2 consent screen, where you can grant access to the google forms API for the google account who owns the form. NB this does not have to be the same google account as the user who created the credentials in the cloud console.

### Security considerations
To ensure only permitted user submissions are accepted, you must set "Collect email addresses by default" to "Verified". This will force the respondent to be signed into googl. Only by doing this can you be sure the respondent is the person who they say they are.

**Regardless of this, all user input to the form must be treated as untrusted, and appropriately escaped on save**
