"""Main entry point
"""
from pyramid.config import Configurator
from sqlalchemy import create_engine
from mailicorn.models import initialize_sql
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.session import UnencryptedCookieSessionFactoryConfig


def main(global_config, **settings):
    authn_policy = AuthTktAuthenticationPolicy(
        secret=settings['auth.secret'])
    authz_policy = ACLAuthorizationPolicy()

    session_factory = UnencryptedCookieSessionFactoryConfig(settings['session.secret'])
    config = Configurator(settings=settings, session_factory=session_factory)
    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(authz_policy)
    config.include("cornice")
    config.scan("mailicorn.views")
    engine = create_engine(settings['sqlalchemy.uri'])
    initialize_sql(engine)
    return config.make_wsgi_app()
