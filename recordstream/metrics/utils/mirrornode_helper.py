import requests
from time import sleep


mainnet_base_url = "https://mainnet-public.mirrornode.hedera.com"
testnet_base_url = "https://testnet.mirrornode.hedera.com"

ft_keys_api = {
    "token_id": "token_id",
    "treasury_account_id": "token_account_number",
    "created_timestamp": "consensus_timestamp",
    "name": "token_name",
    "symbol": "token_symbol",
    "decimals": "token_decimals",
    "initial_supply": "token_initial_supply",
}
nft_keys_api = {
    "token_id": "token_id",
    "symbol": "nft_symbol",
    "treasury_account_id": "account",
    "created_timestamp": "consensus_timestamp",
}


def http_get_with_retry(url, max_retries=3, backoff_factor=0.3, timeout=10):
    """
    Perform an HTTP GET request with retry functionality.

    :param url: The URL to request.
    :param max_retries: The maximum number of retry attempts.
    :param backoff_factor: A backoff factor to apply between attempts.
    :param timeout: The timeout for the request in seconds.
    :return: The response object on success, or None on failure.
    """
    for attempt in range(1, max_retries + 1):
        try:
            response = requests.get(url, timeout=timeout)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            print(f"Attempt {attempt} failed: {e}")
            if attempt == max_retries:
                print("Max retries reached. Request failed.")
                return None
            sleep_time = backoff_factor * (2 ** (attempt - 1))
            print(f"Retrying in {sleep_time} seconds...")
            sleep(sleep_time)



def get_mirrornode(method: str, logger, network: str = "mainnet") -> dict:
    """
    Query Hedera Mirror Node at 100 requests per second

    :param method: API method to query (e.g. /api/v1/account, /api/v1/token)
    More detail can find at https://docs.hedera.com/hedera/sdks-and-apis/rest-api
    :type method: str
    """
    try:
        if network == "mainnet":
            url = mainnet_base_url + method
        elif network == "testnet":
            url = testnet_base_url + method
        else:
            raise ValueError("network must be mainnet or testnet")
        response = http_get_with_retry(url, timeout=30)
        return response.json()
    except (requests.exceptions.Timeout, requests.exceptions.JSONDecodeError):
        logger.warning("Failed to retrieve a response from the MirrorNode API.")
        return {"status": 0}


def parse_token(mirror_token_list, response):
    """parses the tokens of token_type from 1 query iteration to the mirror node

    :param mirror_token_list: cumulative list of tokens returned by the mirror node
    :param response: the mirror node returns up to 25 tokens in each api call
    :return: token list with added tokens after 1 iteration querying the mirror node

    """
    for item in response:
        item.pop("admin_key")
        mirror_token_list.append(item)
    return mirror_token_list


def get_mirrornode_token_list(logger, token_api_endpoint: str = "/api/v1/tokens", network: str = "mainnet"):
    """Aggregates the set of tokens returned by the mirror node

    :token_type: fungible or non-fungible
    :return: set with all tokens of token_type returned by the mirror node
    """
    mirror_token_list = []
    while token_api_endpoint is not None:
        try:
            response = get_mirrornode(token_api_endpoint, logger, network)
            mirror_token_list = parse_token(mirror_token_list, response['tokens'])
            token_api_endpoint = response["links"]["next"]
            logger.info(f"Next was {token_api_endpoint}")
        except Exception as e:
            logger.warning(f"Exception: {e}. Next was {token_api_endpoint} ")

    return mirror_token_list


def parse_token_balance(token_balances, response):
    """parses the tokens of token_type from 1 query iteration to the mirror node

    :param token_balances: cumulative list of tokens returned by the mirror node
    :param response: the mirror node returns up to 25 tokens in each api call
    :return: token list with added tokens after 1 iteration querying the mirror node

    """
    for item in response['balances']:
        token_balances.append(item)
    return token_balances


def get_mirrornode_token_balance(logger, token_id: str, network: str = "mainnet"):
    """Aggregates the set of tokens returned by the mirror node

    :token_type: fungible or non-fungible
    :return: set with all tokens of token_type returned by the mirror node
    """
    token_balances = []
    token_api_endpoint = f"/api/v1/tokens/{token_id}/balances"
    while token_api_endpoint is not None:
        try:
            response = get_mirrornode(token_api_endpoint, logger=logger)
            token_balances = parse_token_balance(token_balances, response)
            import pdb; pdb.set_trace()
            token_api_endpoint = response["links"]["next"]
            logger.info(f"Next was {token_api_endpoint}")
        except Exception as e:
            logger.warning(f"Exception: {e}. Next was {token_api_endpoint} ")
            return None
    return token_balances


def parse_token_details(token_detail_list, response):
    """parses the response from the mirror node, with the right fields to write to the created index

    :param response: response from querying the mirror nodethe mirror node
    """
    if response["type"] == "FUNGIBLE_COMMON":
        _output = {}
        for key, new_key in ft_keys_api.items():
            _output[new_key] = response[key]
        _output["token_number"] = int(response["token_id"].split(".")[-1])
        _output["token_decimals"] = int(_output["token_decimals"])
        _output["token_initial_supply"] = int(_output["token_initial_supply"])
        _output["consensus_timestamp"] = unix_to_timestamp(float(_output["consensus_timestamp"]))
        _output["uuid"] = f"{_output['token_number']}-{_output['consensus_timestamp']}"
        token_detail_list.append(_output)

    if response["type"] == "NON_FUNGIBLE_UNIQUE":
        _output = {}
        for key, new_key in nft_keys_api.items():
            _output[new_key] = response[key]
        _output["consensus_timestamp"] = unix_to_timestamp(float(_output["consensus_timestamp"]))
        _output["uuid"] = f"{_output['token_id']}-{_output['consensus_timestamp']}"
        token_detail_list.append(_output)
    return token_detail_list
