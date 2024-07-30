from eleph import Mastodon

mastodon = Mastodon()
result = mastodon.oauth_authorize(
    response_type="code",
    client_id="",
    redirect_uri="urn:ietf:wg:oauth:2.0:oob"
)
print(result)
