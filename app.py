from flask import Flask, redirect, request, url_for, render_template,session
import spotipy
from spotipy.oauth2 import SpotifyOAuth

SPOTIFY_CLIENT_ID = "240a9f1183934356813d43dd3aeb82ce"
SPOTIFY_CLIENT_SECRET = "2244545b43084ae0a1a56bf52270e829"
SPOTIFY_REDIRECT_URI = "http://127.0.0.1:5000/callback"

app = Flask(__name__)
app.secret_key = 'chiave_per_session'

sp_oauth = SpotifyOAuth(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET,
    redirect_uri=SPOTIFY_REDIRECT_URI,
    scope="user-read-private"
)

@app.route('/')
def login():
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@app.route('/callback')
def callback():
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    session['token_info'] = token_info
    return redirect(url_for('home'))


@app.route('/home')
def home():
    token_info = session.get('token_info', None)
    if not token_info:
        return redirect(url_for('login'))

    sp = spotipy.Spotify(auth=token_info['access_token'])
    user_info = sp.current_user()
    print(user_info)
    return render_template('home.html', user_info=user_info)

if __name__ == '__main__':
    app.run(debug=True)