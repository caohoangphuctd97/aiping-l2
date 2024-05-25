from fastapi import FastAPI

from app.config import config
from app.exceptions.handle_exceptions import configure_exceptions_handlers
from app.middlewares import configure_middlewares
from app.apis import configure_routes
from app.configure_logging import configure_logging


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
configure_logging(config.LOG_LEVEL)

# Configure routes and add dependencies
configure_routes(app)
