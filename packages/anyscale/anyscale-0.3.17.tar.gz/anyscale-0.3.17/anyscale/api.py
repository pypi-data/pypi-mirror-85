import anyscale.client.openapi_client as openapi_client  # type: ignore
from anyscale.client.openapi_client.api.default_api import DefaultApi  # type: ignore
import anyscale.conf
from anyscale.util import load_credentials


def instantiate_api_client(no_cli_token: bool = False) -> DefaultApi:
    if not no_cli_token and anyscale.conf.CLI_TOKEN is None:
        anyscale.conf.CLI_TOKEN = load_credentials()
    configuration = openapi_client.Configuration(host=anyscale.conf.ANYSCALE_HOST)

    if no_cli_token:
        api_client = openapi_client.ApiClient(configuration)
    else:
        api_client = openapi_client.ApiClient(
            configuration, cookie=f"cli_token={anyscale.conf.CLI_TOKEN}"
        )
    api_instance = openapi_client.DefaultApi(api_client)
    return api_instance


def get_api_client() -> DefaultApi:
    if _api_client.api_client is None:
        _api_client.api_client = instantiate_api_client()

    return _api_client.api_client


class _ApiClient(object):
    api_client: DefaultApi = None


_api_client = _ApiClient()
