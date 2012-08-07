from functools import wraps
import os, json
from flask import Flask, render_template, request, g, session, flash, \
     redirect, url_for, abort, send_from_directory, request, Response

from flaskext.openid import OpenID
from flaskext.autoindex import AutoIndex

app = Flask(__name__)
app.secret_key = '\xa5\x10\xbfN3\x1f\t\xd0ec\xa1\xe8\xe7B\x1dU4!\xa1N@\xcf\xfe\xa2'

idx=AutoIndex(app, add_url_rules=False, browse_root="templates")
#idx=AutoIndex(app, add_url_rules=False, browse_root="../..")


oid = OpenID(app)

@app.before_request
def before_request():
    g.user = None
    if 'openid' in session:
        pass

def check_auth():
    if 'DOMAIN' in os.environ:
        if 'openid' in session:
            return True
        return False
    else:
        return True
        
def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if os.environ.get('NO_AUTH', 'False') == 'True':
          return f(*args, **kwargs)

        auth = request.authorization
        if not check_auth():
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated


@app.route('/login', methods=['GET', 'POST'])
@oid.loginhandler
def login():
    domain = os.environ['DOMAIN']
    return oid.try_login("https://www.google.com/accounts/o8/site-xrds?hd=%s" % domain )

@oid.after_login
def create_or_login(resp):
    """This is called when login with OpenID succeeded and it's not
    necessary to figure out if this is the users's first login or not.
    This function has to redirect otherwise the user will be presented
    with a terrible URL which we certainly don't want.
    """
    session['openid'] = resp.identity_url
    return redirect(oid.get_next_url())

@app.route('/logout')
def logout():
    session.pop('openid', None)
    return redirect(oid.get_next_url())

@app.route('/')
@app.route('/<path:path>')
@requires_auth
def autoindex(path="."):
    return idx.render_autoindex(path)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    if 'DEBUG' in os.environ:
        if os.environ['DEBUG'] == 'True':
            DEBUG=True
        else:
            DEBUG=False
    else:
        DEBUG = False
    app.run(debug=DEBUG, host='0.0.0.0', port=port)
