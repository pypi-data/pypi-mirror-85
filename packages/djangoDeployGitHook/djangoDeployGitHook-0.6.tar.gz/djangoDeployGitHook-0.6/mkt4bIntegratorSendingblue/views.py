import json
import logging
from pprint import pprint

import requests
import sib_api_v3_sdk

# Create your views here.
from django.forms import model_to_dict
from django.http import HttpResponse
from django.shortcuts import render
from sib_api_v3_sdk.rest import ApiException

logger = logging.getLogger('django')

# Configure API key authorization: api-key
from django.conf import settings

configuration = sib_api_v3_sdk.Configuration()
configuration.api_key['api-key'] = settings.SENDING_BLUE_API_KEY


# create an instance of the API class

def list_campaign(request):
    # List a campaign\
    filter_api_response_campaigns = ''
    api_instance = sib_api_v3_sdk.EmailCampaignsApi(sib_api_v3_sdk.ApiClient(configuration))
    type = 'classic'

    try:
        api_response = api_instance.get_email_campaigns(type=type)
        if hasattr(request.user, 'userprofile'):
            filter_api_response_campaigns = filter(
                lambda s: s['sender']['email'] == request.user.userprofile.current_business.Email,
                api_response.campaigns)
        else:
            filter_api_response_campaigns = filter(lambda s: s['sender']['email'] == "",
                                                   api_response.campaigns)
        context = {"campaign_page": "active", 'filter_api_response_campaigns': filter_api_response_campaigns}
        return render(request, 'mkt4bIntegratorSendingblue/listCampaign.html', context)
    except ApiException as e:
        print("Exception when calling EmailCampaignsApi->get_email_campaigns: %s\n" % e)


def create_campaign(request):
    # Create a campaign\
    # ------------------
    api_instance = sib_api_v3_sdk.EmailCampaignsApi(sib_api_v3_sdk.ApiClient(configuration))
    # Define the campaign settings\
    email_campaigns = sib_api_v3_sdk.CreateEmailCampaign(
        name="Campaign sent via the API",
        subject="My subject",
        sender={"name": "From name", "email": "mail@marbleriver.pt"},
        # Content that will be sent\
        html_content="Congratulations! You successfully sent this example campaign via the Sendinblue API.",
        # Select the recipients\
        recipients={"listIds": [2]},
        # Schedule the sending in one hour\
        scheduled_at="2021-01-01 00:00:01"
    )
    # Make the call to the client\
    try:
        api_response = api_instance.create_email_campaign(email_campaigns)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling EmailCampaignsApi->create_email_campaign: %s\n" % e)


def campaign_detail(request, pk):
    # Get a campaign\
    try:
        url = "https://api.sendinblue.com/v3/emailCampaigns/" + str(pk)
        headers = {
            "Accept": "application/json",
            "api-key": settings.SENDING_BLUE_API_KEY
        }

        response = requests.request("GET", url, headers=headers)
        response_json = json.loads(response.text)
        context = {"campaign_page": "active", 'api_response_campaign': response_json['htmlContent']}
        return render(request, 'mkt4bIntegratorSendingblue/detailCampaign.html', context)
    except ApiException as e:
        print("Exception when calling EmailCampaignsApi->get_email_campaigns: %s\n" % e)
