import oauth2 as oauth
import time

# Set the API endpoint 
url = "https://api.twitter.com/1.1/friendships/create.json"

# Set the base oauth_* parameters along with any other parameters required
# for the API call.
params = {
    'oauth_version': "1.0",
    'oauth_nonce': oauth.generate_nonce(),
    'oauth_timestamp': int(time.time()),
    'screen_name': 'benm',
    'follow': True
}

# Set up instances of our Token and Consumer. The Consumer.key and 
# Consumer.secret are given to you by the API provider. The Token.key and
# Token.secret is given to you after a three-legged authentication.
token = oauth.Token(key="34409944-0uCTBcWBwwooRGnkuOOV6Z9QnnQ4JK2zDQrysUpTM", secret="0vXZi3JbQTVLOTwPQalwximtAbxuD7hFloerYH4DE")
consumer = oauth.Consumer(key="49Jf6XcYS6nFfDAnD8OxA", secret="Ny7hLvcGNCfafcJykkPpFED350BQ0JjrweOJcVsJs")

# Set our token/key parameters
params['oauth_token'] = tok.key
params['oauth_consumer_key'] = con.key

# Create our request. Change method, etc. accordingly.
req = oauth.Request(method="POST", url=url, parameters=params)

# Sign the request.
signature_method = oauth.SignatureMethod_HMAC_SHA1()
print req.sign_request(signature_method, consumer, token)
