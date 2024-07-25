import json

from flask import Flask, request, redirect

from .logger import log_request
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
    @log_request
    def mastodon_oauth_token():
        app.logger.info(json.dumps(dict(request.values)))
        return oauth.token(**request.args)

    @app.route("/oauth/authorize/")
    @log_request
    def mastodon_oauth_authorize():
        app.logger.info(json.dumps(dict(request.values)))
        try:
            return oauth.authorize(**request.args)
        except HTTPRedirect as exc:
            return redirect(exc.url)

    @app.route("/api/v1/instance")
    @log_request
    def mastodon_v1_instance():
        return mastodon.v1_instance()

    @app.route("/api/v1/apps", methods=["POST"])
    @log_request
    def mastodon_v1_apps():
        return mastodon.v1_apps(**request.form)

    @app.route("/api/v1/accounts/verify_credentials")
    @log_request
    def mastodon_v1_accounts_verify_credentials():
        return mastodon.v1_accounts_verify_credentials()

    @app.route("/api/v1/accounts/<id>/following")
    @log_request
    def mastodon_v1_accounts_following(id: str):
        return mastodon.v1_accounts_following(id=id)

    @app.route("/api/v1/preferences")
    @log_request
    def mastodon_v1_preferences():
        return mastodon.v1_preferences()

    @app.route("/api/v1/timelines/home")
    @log_request
    def mastodon_v1_timelines_home():
        return mastodon.v1_timelines_home()

    @app.route("/api/v2/search")
    @log_request
    def mastodon_v2_search():
        return mastodon.v2_search(**request.args)

    @app.route('/', defaults={'path': ''}, methods=["GET", "POST", "DELETE", "PATCH"])
    @app.route('/<path:path>', methods=["GET", "POST", "DELETE", "PATCH"])
    @log_request
    def default(path):
        return ""

    ###

    return app
