# Python3 Quick start example: list envelopes in the user's account
# Copyright (c) 2018 by DocuSign, Inc.
# License: The MIT License -- https://opensource.org/licenses/MIT

import base64, os
from docusign_esign import ApiClient, EnvelopesApi
import pendulum # pip install pendulum
import pprint

# Settings
# Fill in these constants
#
# Obtain an OAuth access token from https://developers.docusign.com/oauth-token-generator
access_token = '{ACCESS_TOKEN}'
# Obtain your accountId from demo.docusign.com -- the account id is shown in the drop down on the
# upper right corner of the screen by your picture or the default picture. 
account_id = '{ACCOUNT_ID}'; 
base_path = 'https://demo.docusign.net/restapi'

def list_envelopes():
    """
    Lists the user's envelopes created in the last 10 days
    """
    
    #
    # Step 1. Prepare the options object
    #
    from_date = pendulum.now().subtract(days=10).to_iso8601_string()
    #
    # Step 2. Get and display the results
    # 
    api_client = ApiClient()
    api_client.host = base_path
    api_client.set_default_header("Authorization", "Bearer " + access_token)

    envelope_api = EnvelopesApi(api_client)
    results = envelope_api.list_status_changes(account_id, from_date = from_date)
    return results

# Mainline
results = list_envelopes()
print("\nEnvelopes:\n")
pprint.pprint(results, indent=4, width=80)

