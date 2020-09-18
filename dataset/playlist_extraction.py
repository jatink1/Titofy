import spotipy

#from spotipy.oauth2 import SpotifyClientCredentials
from spotipy import oauth2
import csv

usernames = ['mzabdsv3lqwaf49fvuj153gef']
filename = "Playlists_Of_User.csv"

CLIENT_ID = 'XXX'
CLIENT_SECRET = 'XXX'


token = oauth2.SpotifyClientCredentials(client_id = CLIENT_ID  , client_secret = CLIENT_SECRET)
cache_token = token.get_access_token()
sp = spotipy.Spotify(cache_token)

#client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)
#sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def main(): 
    
    for users in usernames:
        
        add_user_playlist(users)

    print("Finished Reading All Playlists.")

def get_tracks_data(tracks, playlist, username):
    
    user_playlist = []
    
    for item_track in tracks['items']:
        
        
        playlist_dict = {}
        playlist_dict['Playlist_Name'] = playlist['name']
        playlist_dict['Username'] = username

        track = item_track['track']
        playlist_dict['Track_Title'] = track['name']
        playlist_dict['Track_ID'] = track['id']
        playlist_dict['Artist'] = track['artists'][0]['name']
        playlist_dict['Duration_ms'] = track['duration_ms']
        playlist_dict['Popularity'] = track['popularity']
        playlist_dict['Explicit'] = track['explicit']
        playlist_dict['Album'] = track['album']['name']

        # get album data not included in playlist
        if track['album']['uri'] is not None: 
            
            album_data = sp.album(track['album']['uri'])
            playlist_dict['Release_Date'] = album_data['release_date']
            playlist_dict['Label'] = album_data['label']

            features = sp.audio_features(track['id'])
            
            playlist_dict['Danceability'] = features[0]['danceability']
            playlist_dict['Energy'] = features[0]['energy']
            playlist_dict['Key'] = features[0]['key']
            playlist_dict['Loudness'] = features[0]['loudness']
            playlist_dict['Speechiness'] = features[0]['speechiness']
            playlist_dict['Acousticness'] = features[0]['acousticness']
            playlist_dict['Instrumentalness'] = features[0]['instrumentalness']
            playlist_dict['Liveness'] = features[0]['liveness']
            playlist_dict['Tempo'] = features[0]['tempo']
            playlist_dict['Time_Signature'] = features[0]['time_signature']

            user_playlist.append(playlist_dict)     
            
    return user_playlist

def add_user_playlist(username):
    
    with open(filename, 'a') as f:
        
        fieldnames = ['Playlist_Name', 'Username', 'Track_Title', 'Track_ID', 'Artist', 
                      'Duration_ms', 'Popularity', 'Explicit', 'Album', 
                      'Release_Date', 'Label', 'Danceability', 'Energy',
                      'Key', 'Loudness', 'Speechiness', 'Acousticness', 'Instrumentalness',
                      'Liveness', 'Tempo', 'Time_Signature']
        
        writer = csv.DictWriter(f, fieldnames)
        writer.writeheader()
        playlists = sp.user_playlists(username)

        print("Getting data from " + username + "'s playlists:")
        playlists = sp.user_playlists(username)

        for playlist in playlists['items']:
            
            user_playlist = []
            
            if playlist['owner']['id'] == username:
                
                print(playlist['name'])

                if 'display_name' in playlist['owner']:
                    
                    disp_name = playlist['owner']['display_name']
                    
                else:
                    
                    disp_name = username

                results = sp.user_playlist(username, playlist['id'], fields="tracks,next")
                tracks = results['tracks']
                user_playlist = user_playlist + get_tracks_data(tracks, playlist, disp_name)
                
                while tracks['next']:
                    
                    tracks = sp.next(tracks)
                    
                    user_playlist = user_playlist + get_tracks_data(tracks, playlist, disp_name)
                    
                writer.writerows(user_playlist)
            
    print()
    
    return user_playlist

if __name__ == '__main__':
    main()