"""Initialize FastAPI app."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer

from .config import Settings

from library.database import models
from library.database.database import engine

def create_app(config=None, aargs=None):
    tags_metadata = [
        {
            "name": "Utilities",
            "description": "Core of the API. Contains functions that are designed for the frontend."
        },
        {
            "name": "Home",
            "description": "Api dedicated to serving the React App for local app client+server deployment.\n This API is not used for web-based deployment."
        },
        {
            "name": "Admin",
            "description": "Api dedicated to server administration"
        },
        {
            "name": "Auth",
            "description": "Api dedicated to Authenticating Users"
        }

    ]
    if Settings.ENV_TYPE == "development":
        app = FastAPI(openapi_tags=tags_metadata)
    else:
        app = FastAPI(openapi_tags=tags_metadata,
                      docs_url=None, redoc_url=None)

    origins = [
        "http://localhost",
        "http://localhost:80",
        "http://localhost:5000"
        "http://localhost:6789",
        "http://localhost:3000",
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    if config:
        Settings.model_copy(update=config)

    models.Base.metadata.create_all(bind=engine)
    Settings.OAUTH_SCHEME = OAuth2PasswordBearer(
        tokenUrl="token",
        scopes={
            "user": "Regular user permissions",
            "admin": "Admin priviledges (Admin API Access)"
        }
    )

    from library.utilities_api import utilities, file_exports
    from library.admin_api import api as admin_api
    from library.auth_api import api as auth_api
    from library.auth_api.backend import auth_backend
    
    app.include_router(utilities.utils_api)
    app.include_router(file_exports.utils_api)
    app.include_router(admin_api.admin_api)
    app.include_router(
        auth_api.fastapi_users.get_auth_router(auth_backend)
        prefix="/auth/jwt",
        tags=["auth"],
    )


    # Only deploy react build only if it is a client+server deployment
    if Settings.ENV_TYPE != "server" or Settings.ENV_TYPE == "development":
        from library.home_api import home
        # NOTE: REGISTER home_router LAST AS IT HOSTS A CATCH ALL ROUTE AND WILL OVERRIDE OTHER ROUTES
        app.include_router(home.home_router)

    return app
