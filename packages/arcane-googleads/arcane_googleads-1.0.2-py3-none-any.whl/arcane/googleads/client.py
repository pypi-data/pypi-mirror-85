from google.ads.google_ads.client import GoogleAdsClient
from google.ads.google_ads.errors import GoogleAdsException
import backoff
from arcane.core.exceptions import GOOGLE_EXCEPTIONS_TO_RETRY

from .exceptions import GoogleAdsAccountLostAccessException
from .helpers import make_request_account_id

_GOOGLE_ADS_VERSION = "v5"


def get_google_ads_client(credentials_path: str) -> GoogleAdsClient:
    return GoogleAdsClient.load_from_storage(credentials_path)


def get_google_ads_service(service_name: str, google_ads_client: GoogleAdsClient, version: str = _GOOGLE_ADS_VERSION):
    return google_ads_client.get_service(service_name, version=version)

@backoff.on_exception(backoff.expo, GOOGLE_EXCEPTIONS_TO_RETRY, max_tries=5)
def check_access_account(account_id: str, google_ads_client: GoogleAdsClient):
    """From an account id check if Arcane has access to it"""
    google_ads_service = get_google_ads_service('GoogleAdsService', google_ads_client)

    query = f"""
        SELECT
          customer_client.manager
        FROM customer_client
        WHERE customer_client.id = '{account_id}'"""
    try:
        response = list(google_ads_service.search(account_id, query))[0]
    except GoogleAdsException as err:
        if "USER_PERMISSION_DENIED" in str(err):
                raise GoogleAdsAccountLostAccessException(f"We cannot access your Google Ads account with the id: {account_id}. Are you sure you granted access?")
        elif "CUSTOMER_NOT_FOUND" in str(err):
            raise GoogleAdsAccountLostAccessException(f"We cannot find this account ({account_id}). Are you sure you entered the correct id?")
        else:
            raise GoogleAdsAccountLostAccessException(
                f"We cannot access this account ({account_id}). Are you sure you entered the correct id?")

    if response.customer_client.manager:
        raise GoogleAdsAccountLostAccessException('This account ID is a MCC. Please enter a Google Ads Account.')
