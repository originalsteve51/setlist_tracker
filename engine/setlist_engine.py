import cmd
import requests
import json
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth

from openai import OpenAI


web_controller_url = os.environ['WEB_CONTROLLER_URL']
print('Web controller url: ', web_controller_url)

set_data = []

#-----------------------------------------------------------
# Spotify is a class that provides access to the Spotify API
# The spotipy library performs its magic here by using values
# found in the environment to authenticate the user. Once
# authenticated, the api can be called.
# This depends on the following environment variable values, which
# should be set by a shell script.
# export SPOTIPY_CLIENT_ID=
# export SPOTIPY_CLIENT_SECRET=
# export SPOTIPY_REDIRECT_URI="http://127.0.0.1:8080"
#-----------------------------------------------------------
class Spotify():
    def __init__(self):
        ascope = 'user-read-currently-playing,\
                playlist-modify-private,\
                user-read-playback-state,\
                user-modify-playback-state'
        ccm=SpotifyOAuth(scope=ascope, open_browser=True)
        self.sp = spotipy.Spotify(client_credentials_manager=ccm)

class Playlist():
    def __init__(self, sp, ai):
        self.sp = sp
        self.ai = ai
        self.track_set = set(())

    def get_playlists(self):
        results = self.sp.current_user_playlists(limit=50)
        lists = {}
        for i, item in enumerate(results['items']):
            lists[str(i)] = [item['name'], item['id']]
        return lists

    def process_playlist(self, pl_index):
        playlist = self.get_playlists()[f"{pl_index}"]
        print(f'{playlist[0]}')
        pl_id = f'spotify:playlist:{playlist[1]}'

        self.playlist_processing(pl_id)

    def playlist_processing(self, pl_id):
        global set_data

        set_data.clear()
        
        offset = 0
        response = self.sp.playlist_items(pl_id,
                                    offset=offset,
                                    fields='items.track.name, \
                                            items.track.id, \
                                            items.track.artists.name, \
                                            items.track.album.name, \
                                            items.track.album.id, \
                                            total',
                                    additional_types=['track'])

        if len(response['items']) != 0:
            # print(response['items'][0])
            album_name = 'album_name'
            year_released = '2012'
            for idx in range(0, len(response['items'])):
                row_data = dict()
                track = response['items'][idx]['track']
                artist_name = response['items'][idx]['track']['artists'][0]['name']
                album_name = response['items'][idx]['track']['album']['name']
                album_id = response['items'][idx]['track']['album']['id']
                track_id = track['id']
                #track_urn = f'spotify:track:{track_id}'
                #track_info = sp.track(track_urn)
                # artist_name = track_info['album']['artists'][0]['name']
                # print(track['name'], artist_name)
                row_data['song_name'] = track['name']
                row_data['artist_name'] = artist_name
                row_data['album_name'] = album_name
                # row_data['year_released'] = '1998'

                album_response = self.sp.album(album_id)
                release_date = 'Unknown'
                if 'release_date' in album_response.keys():
                    release_date = album_response['release_date']
                else:
                    release_date = 'Unknown'
                row_data['year_released'] = release_date
                
                row_data['song_info'] = self.ai.get_song_info(artist_name, row_data['song_name'])
                set_data.append(row_data)          
              

class OpenAIAccessor():
    def __init__(self):
        api_key = os.getenv('OPENAI_API_KEY')
        self.url='https://api.openai.com/v1/chat/completions'
        self.headers={
                        'Authorization':f'Bearer {api_key}',
                        'Content-Type':'application/json'
                    }

    def get_song_info(self, artist, song_name):
        
        data = {
            'model': 'gpt-4o-mini',
            'messages': [{'role': 'user', 
                        'content': f"Give me history including lyrical themes of the \
                                    {artist}'s song '{song_name}', \
                                    max length 400 words, using words that a fifth grader can understand. Break this into paragraphs \
                                    with <p> at the start of each paragraph and </p> \
                                    at the end of each paragraph."}],
            'max_tokens':500,
            'temperature':0.8
        }
        print('-------> get_song_info called')
        raw_info = requests.post(self.url, headers=self.headers, json=data)
        json_info = json.loads(raw_info.text)

        return json_info['choices'][0]['message']['content']




class CommandProcessor(cmd.Cmd):
    def __init__(self):
        super(CommandProcessor, self).__init__()
        spotify = Spotify()
        self.sp = spotify.sp
        self.openai = OpenAIAccessor() 

        self.pl = Playlist(spotify.sp, self.openai)
        
    prompt = '(Issue a command)'

    def do_test(self, _):
        x = self.openai.get_song_info("Beatles", "Octupus's Garden")
        print(x)
        
    
    def do_webload(self, _):
        print(f'Loading set list data to web controller')

        requests.post(web_controller_url+'/load_setlist',
                            json=json.dumps(set_data))

    def do_playlists(self, sub_command=None):
        """Display all Spotify playlists for the authorized Spotify user."""
        playlists = self.pl.get_playlists()
        print('\nThese are your playlists:')
        for k in playlists.keys():
            print(f'{k}: {playlists[f"{k}"][0]}')

    def do_stagelist(self, list_number):
        """Show the names of tracks in a Spotify playlist."""
        if list_number:
            self.pl.process_playlist(list_number)
        else:
            print('You must enter the number of a playlist to stage its tracks')

    def do_quit(self, args):
        """ 
        Quit the game, stopping the music player if it's playing and
        cleaning up as necessary. The state of a game in progress is saved
        so you can use continuegame to resume a game if you want.
        """
        raise ExitCmdException()

#-------------------------------------------------------------------
# ExitCmdException class - Just so we have a good name when breaking
# out of the command loop with an Exception
#-------------------------------------------------------------------
class ExitCmdException(Exception):
    pass 

def display_general_exception(e):
    exception_name = e.__class__.__name__
    if exception_name == 'ReadTimeout' or exception_name == 'ConnectionError':
        print(f'\n{exception_name}:\nA network error occurred, possibly the web app is not running.')
    else:
        print(f'\n{exception_name}:\nAn unexpected error occurred.')


if __name__ == '__main__':
    continue_running = True
    cp = None
    while continue_running:
        # Enter the command loop, handling Exceptions that break it. Some Exceptions
        # can be handled, like losing the network. We give the user a chance
        # to correct such errors. If the user believes an Exception
        # has been corrected, the command loop will restart.
        try:
            if cp is None:
                cp = CommandProcessor()
            cp.cmdloop()
        except KeyboardInterrupt:
            print('Interrupted by ctrl-C, attempting to clean up first')
            try:
                cleanup_before_exiting(cp)
                sys.exit(0)
            except SystemExit:
                os._exit(0)
        except Exception as e:
            exception_name = e.__class__.__name__
    
            if exception_name == 'ExitCmdException':
                continue_running = False
                print('\nExiting the program...')
                continue
            else:
                display_general_exception(e)
            
            choice = input('Try correcting this problem and press "Y" to try again, or any other key to exit. ')
            if choice.upper() != 'Y':
                continue_running = False
                print('Exiting the program')        
