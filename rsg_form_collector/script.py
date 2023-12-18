import json
import tomllib

import apiclient
import google.oauth2
import google_auth_oauthlib.flow
import httplib2

SCOPES = [
    "https://www.googleapis.com/auth/forms.responses.readonly",
]
DISCOVERY_DOC = "https://forms.googleapis.com/$discovery/rest?version=v1"


def main():
    """Get some data from a google form."""
    # Load some basic config from a file
    with open("./config.toml", "rb") as file:
        config = tomllib.load(file)

    # Load a list of allowed respondents from file.
    with open("./allowed_respondents.json", "r", encoding="utf-8") as file:
        allowed_respondents = json.load(file)

    # Do authentication to google.
    try:
        credentials = google.oauth2.credentials.Credentials.from_authorized_user_file(
            "./credentials.json"
        )
        if not credentials.valid:
            credentials.refresh(httplib2.Http())
    except FileNotFoundError:
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
            "./client_secret.json",
            scopes=SCOPES,
            redirect_uri="urn:ietf:wg:oauth:2.0:oob",
        )
        flow.run_local_server(port=8090)

        with open("credentials.json", "w", encoding="utf-8") as file:
            file.write(flow.credentials.to_json())
        credentials = flow.credentials

    # Build an endpoint to the google API.
    service = apiclient.discovery.build(
        "forms",
        "v1",
        discoveryServiceUrl=DISCOVERY_DOC,
        static_discovery=False,
        credentials=credentials,
    )

    # Get the content of the form.
    result = service.forms().responses().list(formId=config["form_id"]).execute()

    responses = result["responses"]
    # Filter to only allowed respondents.
    responses = [x for x in responses if x["respondentEmail"] in allowed_respondents]

    # Then do something with the responses.
    for response in responses:
        print(json.dumps(response, indent=2))


if __name__ == "__main__":
    main()
