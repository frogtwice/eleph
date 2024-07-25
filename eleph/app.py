import json
import logging

from flask import Flask, request, redirect

from .mastodon import Mastodon
from .oauth import OAuth, HTTPRedirect


def create_app(uri: str):
    app = Flask("eleph")
    mastodon = Mastodon(uri)
    oauth = OAuth()

    ############
    # MASTODON #
    ############

    @app.route("/oauth/token", methods=["POST"])
    def mastodon_oauth_token():
        app.logger.info(json.dumps(dict(request.values)))
        return oauth.token(**request.args)

    @app.route("/oauth/authorize/")
    def mastodon_oauth_authorize():
        app.logger.info(json.dumps(dict(request.values)))
        try:
            return oauth.authorize(**request.args)
        except HTTPRedirect as exc:
            return redirect(exc.url)

    @app.route("/api/v1/instance")
    def mastodon_v1_instance():
        return mastodon.v1_instance()

    @app.route("/api/v1/apps", methods=["POST"])
    def mastodon_v1_apps():
        return mastodon.v1_apps(**request.form)

    @app.route("/api/v1/accounts/verify_credentials")
    def mastodon_v1_accounts_verify_credentials():
        return mastodon.v1_accounts_verify_credentials()

    @app.route("/api/v1/accounts/<id>/following")
    def mastodon_v1_accounts_following(id: str):
        return mastodon.v1_accounts_following(id=id)

    @app.route("/api/v1/preferences")
    def mastodon_v1_preferences():
        return mastodon.v1_preferences()

    @app.route("/api/v1/timelines/home")
    def mastodon_v1_timelines_home():
        return mastodon.v1_timelines_home()

    @app.route("/api/v2/search")
    def mastodon_v2_search():
        return mastodon.v2_search(**request.args)

    ###

    return app
