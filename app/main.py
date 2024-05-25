from fastapi import FastAPI

from .config import config
from .exceptions.handle_exceptions import configure_exceptions_handlers
from .middlewares import configure_middlewares

from app.apis import configure_routes


# Create instance of application
app = FastAPI(
    title=config.APPLICATION_NAME,
    description=config.DESCRIPTION,
    version="0.0.1",
    debug=False,
    docs_url=f"{config.OPENAPI_PREFIX}/docs",
)
# Update and set up configs
configure_exceptions_handlers(app)
configure_middlewares(app)

# Configure routes and add dependencies
configure_routes(app)


