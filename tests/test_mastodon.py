from eleph import Mastodon, OAuth

mastodon = Mastodon()
oauth = OAuth()
result = oauth.authorize(
    response_type="code",
    client_id="",
    redirect_uri="urn:ietf:wg:oauth:2.0:oob"
)
print(result)
