import requests


class TransferwiseClient(object):
    """Fetch the conversion rate for source and target currencies
    from Transferwise."""

    _exchange_rate_url = 'https://api.transferwise.com/v1/rates?source={0}&target={1}'
    # _auth_token_url = 'https://api.transferwise.com/v1/rates?source={0}&target={1}'

    def __init__(self):
        """init"""
        self._thread = None

    def _get_conversion_rate(self, source, target, token):
        """
        Fetch conversion rate from Transferwise

        :param source: source currency code - SEK
        :param target: target currency code - INR
        :param token: Transferwise bearer token
        :return: JSON string with conversion rate and time
        """
        response = requests.get(url=self._exchange_rate_url.format(source, target), headers=_get_headers(token))
        return response

    def get_conversion_rate(self, source, target, token):
        """
        Fetch conversion rate from Transferwise

        :param source: source currency code - SEK
        :param target: target currency code - INR
        :param token: Transferwise bearer token
        :return: JSON string with conversion rate and time
        """
        return self._get_conversion_rate(source, target, token)

    def load_auth_token(self, auth):
        """The program will try and find the access token in the following manner
        1. System Variable named TCR
        2. Configuration file - located at ~/.tcr on linux or %HOMEDRIVE%%HOMEPATH%/.tcr on windows"""

        token = auth.get_auth_from_env()
        if token is not None:
            return token
        else:
            token = auth.get_auth_from_property()

        if token is not None:
            return token

        raise FileNotFoundError("No token found.")


def _get_headers(token):
    return {'Authorization': 'Bearer ' + token}
