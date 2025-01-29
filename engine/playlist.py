import spotipy
import os

max_ai_calls_for_info = int(os.environ['MAX_AI_CALLS_FOR_INFO'])




class Playlist():
    def __init__(self, sp, ai):
        self.sp = sp
        self.ai = ai
        self.set_data = []
        self.playlist_name = ''


    def get_playlists(self):
        results = self.sp.current_user_playlists(limit=50)
        lists = {}
        for i, item in enumerate(results['items']):
            lists[str(i)] = [item['name'], item['id']]
        return lists

    def process_playlist(self, pl_index, call_ai):

        playlist = self.get_playlists()[f"{pl_index}"]

        self.playlist_name = f'{playlist[0]}'
        
        pl_id = f'spotify:playlist:{playlist[1]}'

        self.playlist_processing(pl_id, call_ai)

    def playlist_processing(self, pl_id, call_ai):

        self.set_data.clear()
        
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
            #print(response['items'][0])
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
                row_data['song_name'] = track['name']
                row_data['artist_name'] = artist_name
                row_data['album_name'] = album_name
                row_data['id'] = track_id
                
                album_response = self.sp.album(album_id)
                release_date = 'Unknown'
                if 'release_date' in album_response.keys():
                    release_date = album_response['release_date']
                row_data['year_released'] = release_date
                
                if call_ai:
                    if idx < max_ai_calls_for_info:
                        row_data['song_info'] = self.ai.get_song_info(artist_name, row_data['song_name'])
                    else:
                        row_data['song_info'] = f'{idx}: Not available due to test mode'
                else:
                    row_data['song_info'] = f'{idx}: Not requested by caller'
                self.set_data.append(row_data)  
                song_name_len = len(row_data['song_name'])

                tab_str = ''
                print(f"{idx}, {row_data['song_name']}, {tab_str} {row_data['artist_name']}. '\n',{row_data['song_info']}")

