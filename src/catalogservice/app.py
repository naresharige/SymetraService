from fastapi import Depends, FastAPI, Request, status
from starlette.config import Config

from catalogservice.fixtures.fixtures import products
from catalogservice.models.health import HealthResponse
from catalogservice.models.products import ProductsResponse
from catalogservice.services.auth import AuthService

config = Config(".env")

auth_service = AuthService(config)

app = FastAPI(
    title="Symetra Financial",
    description="Leverage OKTA to protect Symetra Product APIs",
    version="1.0.0"
)


@app.get("/health", response_model=HealthResponse, status_code=status.HTTP_200_OK)
def get_health():
    """
    Check the health status of the service.

    Returns:
        dict: A dictionary indicating the service status.
    """
    return {"status": "OK"}


@app.post("/token", status_code=status.HTTP_201_CREATED)
def login(request: Request):
    """
    Get an authentication token.

    Args:
        request (Request): The HTTP request object containing the authorization header.

    Returns:
        dict: The authentication token.
    """
    return auth_service.retrieve_token(
        request.headers["authorization"],
        config("OKTA_ISSUER"),
        "products"
    )


@app.get("/products", response_model=ProductsResponse, status_code=status.HTTP_200_OK)
def get_products(valid: bool = Depends(auth_service.validate)):
    """
    Get the list of products.

    Args:
        valid (bool, optional): Indicates if the user is valid. Defaults to Depends(auth_service.validate).

    Returns:
        ProductsResponse: The response containing the list of products.
    """
    return products
