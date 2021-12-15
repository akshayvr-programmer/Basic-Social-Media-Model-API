import os

import typing
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse, PlainTextResponse
from starlette.datastructures import Headers
from starlette.exceptions import ExceptionMiddleware
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import Response
from starlette.types import ASGIApp

from supertokens_python import init, get_all_cors_headers
from supertokens_python.framework.fastapi import Middleware
from supertokens_python.recipe import session, thirdpartyemailpassword, thirdparty, emailpassword
from supertokens_python.recipe.session import Session
from supertokens_python.recipe.session.framework.fastapi import verify_session
from supertokens_python.recipe.thirdparty import Github, Google, Apple, Discord, GoogleWorkspaces

load_dotenv()

app = FastAPI(debug=True)
app.add_middleware(Middleware)
os.environ.setdefault('SUPERTOKENS_ENV', 'testing')


def get_api_port():
    return '8000'


def get_website_port():
    return '3000'


def get_website_domain():
    return 'http://localhost:' + get_website_port()


init({
    'supertokens': {
        'connection_uri': "https://try.supertokens.io",
    },
    'framework': 'fastapi',
    'app_info': {
        'app_name': "SuperTokens",
        'api_domain': "0.0.0.0:" + get_api_port(),
        'website_domain': get_website_domain(),
    },
    'recipe_list': [
        session.init({}),
        thirdparty.init({
            'sign_in_and_up_feature': {
                'providers': [
                    Github(
                        is_default=True,
                        client_id=os.environ.get('GITHUB_CLIENT_ID'),
                        client_secret=os.environ.get('GITHUB_CLIENT_SECRET')
                    ), Github(
                        client_id=os.environ.get('GITHUB_CLIENT_ID_MOBILE'),
                        client_secret=os.environ.get('GITHUB_CLIENT_SECRET_MOBILE')
                    ), Apple(
                        is_default=True,
                        client_id=os.environ.get('APPLE_CLIENT_ID'),
                        client_key_id=os.environ.get('APPLE_KEY_ID'),
                        client_team_id=os.environ.get('APPLE_TEAM_ID'),
                        client_private_key=os.environ.get('APPLE_PRIVATE_KEY')
                    ), Apple(
                        client_id=os.environ.get('APPLE_CLIENT_ID_MOBILE'),
                        client_key_id=os.environ.get('APPLE_KEY_ID'),
                        client_team_id=os.environ.get('APPLE_TEAM_ID'),
                        client_private_key=os.environ.get('APPLE_PRIVATE_KEY')
                    ), GoogleWorkspaces(
                        is_default=True,
                        client_id=os.environ.get('GOOGLE_WORKSPACES_CLIENT_ID'),
                        client_secret=os.environ.get('GOOGLE_WORKSPACES_CLIENT_SECRET')
                    ), Discord(
                        is_default=True,
                        client_id=os.environ.get('DISCORD_CLIENT_ID'),
                        client_secret=os.environ.get('DISCORD_CLIENT_SECRET')
                    )
                ]
            }
        }),
        emailpassword.init(),
        thirdpartyemailpassword.init({
            'providers': [
                Google(
                    is_default=True,
                    client_id=os.environ.get('GOOGLE_CLIENT_ID'),
                    client_secret=os.environ.get('GOOGLE_CLIENT_SECRET')
                ), Google(
                    client_id=os.environ.get('GOOGLE_CLIENT_ID_MOBILE'),
                    client_secret=os.environ.get('GOOGLE_CLIENT_SECRET')
                ), Github(
                    is_default=True,
                    client_id=os.environ.get('GITHUB_CLIENT_ID'),
                    client_secret=os.environ.get('GITHUB_CLIENT_SECRET')
                ), Github(
                    client_id=os.environ.get('GITHUB_CLIENT_ID_MOBILE'),
                    client_secret=os.environ.get('GITHUB_CLIENT_SECRET_MOBILE')
                ), Apple(
                    is_default=True,
                    client_id=os.environ.get('APPLE_CLIENT_ID'),
                    client_key_id=os.environ.get('APPLE_KEY_ID'),
                    client_team_id=os.environ.get('APPLE_TEAM_ID'),
                    client_private_key=os.environ.get('APPLE_PRIVATE_KEY')
                ), Apple(
                    client_id=os.environ.get('APPLE_CLIENT_ID_MOBILE'),
                    client_key_id=os.environ.get('APPLE_KEY_ID'),
                    client_team_id=os.environ.get('APPLE_TEAM_ID'),
                    client_private_key=os.environ.get('APPLE_PRIVATE_KEY')
                ), GoogleWorkspaces(
                    is_default=True,
                    client_id=os.environ.get('GOOGLE_WORKSPACES_CLIENT_ID'),
                    client_secret=os.environ.get('GOOGLE_WORKSPACES_CLIENT_SECRET')
                ), Discord(
                    is_default=True,
                    client_id=os.environ.get('DISCORD_CLIENT_ID'),
                    client_secret=os.environ.get('DISCORD_CLIENT_SECRET')
                )
            ]
        })
    ],
    'telemetry': False
})


app.add_middleware(ExceptionMiddleware, handlers=app.exception_handlers)


@app.get('/sessioninfo')
async def get_session_info(session_: Session = Depends(verify_session())):
    return JSONResponse({
        'sessionHandle': session_.get_handle(),
        'userId': session_.get_user_id(),
        'accessTokenPayload': session_.get_access_token_payload(),
        # 'sessionData': await session_.get_session_data()
    })


@app.exception_handler(405)
def f_405(_, e):
    return PlainTextResponse('', status_code=404)


class CustomCORSMiddleware(CORSMiddleware):
    def __init__(
        self,
        app_: ASGIApp,
        allow_origins: typing.Sequence[str] = (),
        allow_methods: typing.Sequence[str] = ("GET",),
        allow_headers: typing.Sequence[str] = (),
        allow_credentials: bool = False,
        allow_origin_regex: str = None,
        expose_headers: typing.Sequence[str] = (),
        max_age: int = 600,
    ) -> None:
        super().__init__(app_, allow_origins, allow_methods, allow_headers, allow_credentials, allow_origin_regex,
                         expose_headers, max_age)

    def preflight_response(self, request_headers: Headers) -> Response:
        result = super().preflight_response(request_headers)
        if result.status_code == 200:
            result.headers.__delitem__('content-type')
            result.headers.__delitem__('content-length')
            return Response(status_code=204, headers=dict(result.headers))
        return result


app = CustomCORSMiddleware(
    app_=app,
    allow_origins=[
        get_website_domain()
    ],
    allow_credentials=True,
    allow_methods=["GET", "PUT", "POST", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["Content-Type"] + get_all_cors_headers(),
)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=get_api_port())