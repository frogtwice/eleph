from flask import Flask, request, redirect

from .logger import log_all, logger
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
    @log_all
    def mastodon_oauth_token():
        return oauth.token(**request.args)

    @app.route("/oauth/authorize/")
    @log_all
    def mastodon_oauth_authorize():
        try:
            return oauth.authorize(**request.args)
        except HTTPRedirect as exc:
            return redirect(exc.url)

    @app.route("/api/v1/instance")
    @log_all
    def mastodon_v1_instance():
        return mastodon.v1_instance()

    @app.route("/api/v1/apps", methods=["POST"])
    @log_all
    def mastodon_v1_apps():
        return mastodon.v1_apps(**request.form)

    @app.route("/api/v1/accounts/verify_credentials")
    @log_all
    def mastodon_v1_accounts_verify_credentials():
        return mastodon.v1_accounts_verify_credentials()

    @app.route("/api/v1/accounts/<id>/following")
    @log_all
    def mastodon_v1_accounts_following(id: str):
        return mastodon.v1_accounts_following(id=id)

    @app.route("/api/v1/announcements")
    @log_all
    def mastodon_v1_announcements():
        return mastodon.v1_announcements()

    @app.route("/api/v1/conversations")
    @log_all
    def mastodon_v1_conversations():
        return mastodon.v1_conversations()

    @app.route("/api/v1/markers")
    @log_all
    def mastodon_v1_markers():
        return mastodon.v1_markers()

    @app.route("/api/v1/notifications")
    @log_all
    def mastodon_v1_notifications():
        return mastodon.v1_notifications()

    @app.route("/api/v1/preferences")
    @log_all
    def mastodon_v1_preferences():
        return mastodon.v1_preferences()

    @app.route("/api/v1/timelines/home")
    @log_all
    def mastodon_v1_timelines_home():
        return mastodon.v1_timelines_home()

    @app.route("/api/v1/timelines/public")
    @log_all
    def mastodon_v1_timelines_public():
        return mastodon.v1_timelines_public()

    @app.route("/api/v2/search")
    @log_all
    def mastodon_v2_search():
        return mastodon.v2_search(**request.args)

    @app.route('/', defaults={'path': ''}, methods=["GET", "POST", "DELETE", "PATCH"])
    @app.route('/<path:path>', methods=["GET", "POST", "DELETE", "PATCH"])
    @log_all
    def default(path):
        logger.info("NOT FOUND")
        return "Not Found.", 404

    ###

    return app
