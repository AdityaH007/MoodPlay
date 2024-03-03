import spotipy
from spotipy.oauth2 import SpotifyOAuth
import random
import webbrowser


SPOTIPY_CLIENT_ID = '27da84882ead460aa3b0c7c30148d253'
SPOTIPY_CLIENT_SECRET = 'b4669cb793f3498db3ce2ada64e6d940'
SPOTIPY_REDIRECT_URI = 'http://localhost:8888/callback'


sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                                               client_secret=SPOTIPY_CLIENT_SECRET,
                                               redirect_uri=SPOTIPY_REDIRECT_URI,
                                               scope="playlist-modify-public"))


def create_and_populate_playlist(mood, language):
    
    playlist_name = f"{mood.capitalize()} {language.capitalize()} Playlist"
    playlist_description = f"A dynamic playlist for a {mood} mood with {language} songs."

    playlist = sp.user_playlist_create(sp.me()['id'], name=playlist_name, public=True, description=playlist_description)
    playlist_id = playlist['id']

    
    add_random_tracks_to_playlist(playlist_id, mood, language)

    return playlist_id, playlist_name


def add_random_tracks_to_playlist(playlist_id, mood, language, num_tracks=20):
    
    results = sp.search(q=f"mood:{mood} language:{language}", type='track', limit=num_tracks)
    
    
    track_uris = [track['uri'] for track in results['tracks']['items']]
    
    
    random.shuffle(track_uris)
    
    
    sp.playlist_add_items(playlist_id, track_uris)


def main():
    
    user_mood = input("Enter your mood (e.g., Happy, Chill): ")

    
    user_language = input("Enter your preferred language (e.g., English, Spanish): ")

    
    playlist_id, playlist_name = create_and_populate_playlist(user_mood, user_language)

    if playlist_id:
        
        playlist = sp.playlist(playlist_id)
        playlist_link = playlist['external_urls']['spotify']

        
        print(f"Dynamic playlist '{playlist_name}' created and populated for your mood and language!")
        print(f"Playlist Link: {playlist_link}")

        
        webbrowser.open(playlist_link)
    else:
        print("Sorry, couldn't create a playlist for the given mood and language.")

if __name__ == "__main__":
    main()
