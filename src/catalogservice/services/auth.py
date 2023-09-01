import httpx
from fastapi import Depends, HTTPException
from okta_jwt.jwt import validate_token as validate_locally
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


class AuthService:
    def __init__(self, config):
        self.config = config

    @staticmethod
    def _get_headers(authorization):
        """
        Generate HTTP headers for requests.

        Args:
            authorization (str): The authorization header.

        Returns:
            dict: HTTP headers.
        """
        return {
            'accept': 'application/json',
            'authorization': authorization,
            'cache-control': 'no-cache',
            'content-type': 'application/x-www-form-urlencoded'
        }

    def retrieve_token(self, authorization, issuer, scope='products'):
        """
        Retrieve a token from the authorization server.

        Args:
            authorization (str): The authorization header.
            issuer (str): The issuer URL.
            scope (str, optional): The scope of the token. Defaults to 'products'.

        Returns:
            dict: The token response.
        """
        headers = self._get_headers(authorization)
        data = {
            'grant_type': 'client_credentials',
            'scope': scope,
        }
        url = issuer + '/v1/token'

        response = httpx.post(url, headers=headers, data=data)

        if response.status_code == httpx.codes.OK:
            return response.json()
        else:
            raise HTTPException(status_code=httpx.codes.BAD_REQUEST, detail=response.text)

    def validate_remotely(self, token, issuer, clientId, clientSecret):
        """
        Validate a token remotely with the identity provider.

        Args:
            token (str): The token to validate.
            issuer (str): The issuer URL.
            clientId (str): The client ID.
            clientSecret (str): The client secret.

        Returns:
            bool: True if the token is valid, False otherwise.
        """
        headers = self._get_headers('')
        data = {
            'client_id': clientId,
            'client_secret': clientSecret,
            'token': token,
        }
        url = issuer + '/v1/introspect'

        response = httpx.post(url, headers=headers, data=data)

        return response.status_code == httpx.codes.OK and response.json()['active']

    def validate(self, token: str = Depends(oauth2_scheme)):
        """
        Validate a token locally.

        Args:
            token (str, optional): The token to validate. Defaults to Depends(oauth2_scheme).

        Returns:
            bool: True if the token is valid, False otherwise.
        """
        try:
            res = validate_locally(
                token,
                self.config('OKTA_ISSUER'),
                self.config('OKTA_AUDIENCE'),
                self.config('OKTA_CLIENT_ID')
            )
            return bool(res)
        except Exception:
            raise HTTPException(status_code=httpx.codes.FORBIDDEN)
