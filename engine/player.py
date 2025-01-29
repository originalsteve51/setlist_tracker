
import spotipy
import random



#-------------------------------------------------------------------
# Player class
#-------------------------------------------------------------------
class Player():
    def __init__(self, sp):
        self.active_player = None
        self.sp = sp
        self.unplayed_track_indexes = []
        self.track_ids = []
        self.played_track_indexes = []

        self.paused = False
        self.paused_at_ms = 0
        self.current_track_idx = None

        if not self.show_available_players():
            print('\n\nNo Players are started!\nYou must start one before attempting to play a track!')

        
    def add_from_playlist(self, playlist):
        for idx, item in enumerate(playlist.set_data):
            self.track_ids.append(item['id'])
            self.unplayed_track_indexes.append(idx)
        print(self.track_ids)

    def show_available_players(self, list_all_players=True):
        has_available = False
        res = self.sp.devices()
        player_count = len(res['devices'])
        print(f'Your account is associated with {player_count} players.')
        for idx in range(player_count):
            if list_all_players:
                player_data = f"{res['devices'][idx]['name']},{res['devices'][idx]['type']}"
                active_msg = 'Inactive'
                if res['devices'][idx]['is_active']:
                    active_msg = 'Active'
                print(f'{idx}: {player_data}, {active_msg}')
            if res['devices'][idx]['is_active']: # and self.active_player is None:
                self.active_player = res['devices'][idx]['id']
                print(f'Selected active music player: ', {res['devices'][idx]['name']})
                has_available = True 
        return has_available

    def play_track(self, track_id, track_idx):
        try:
            # Set the repeat mode to off, otherwise the track will repeat
            # and this is not what I think we want.
            self.current_track_idx = track_idx
            self.sp.repeat(state='off', device_id=self.active_player)
            self.sp.start_playback(uris=[f'spotify:track:{track_id}'], 
                            device_id=self.active_player)
        except Exception as e:
            display_player_exception(e)

    def resume_track(self, track_id, position_ms):
        try:
            self.sp.start_playback(uris=[f'spotify:track:{track_id}'], 
                            device_id=self.active_player, 
                            position_ms=position_ms)
        except Exception as e:
            display_player_exception(e)

    def set_volume(self, volume_pct):
        self.sp.volume(volume_pct)

    def pause_playback(self):
        self.sp.pause_playback()
        self.paused_at_ms = self.currently_playing()[0]
        self.paused = True
        print(f'Paused at {self.paused_at_ms}, current track idx: {self.current_track_idx}')

    def resume(self):
        if self.paused_at_ms:
            track_to_resume = self.track_ids[self.current_track_idx]
            print(f'track resume id: {track_to_resume}')
            self.resume_track(track_to_resume, self.paused_at_ms)
            self.paused_at_ms = None
        else:
            print('Nothing was paused, so cannot resume!')


    def currently_playing(self):
        track = self.sp.current_user_playing_track()
        is_playing = False
        progress = 0
        if track:
            is_playing = track['is_playing']
            progress = track['progress_ms']
        return progress, is_playing






    def play_next_track(self, testmode=False):
        if len(self.unplayed_track_indexes) == 0:
            print('All tracks have been played.')
            return None

        track_idx = random.choice(self.unplayed_track_indexes)

        self.unplayed_track_indexes.remove(track_idx)
        self.played_track_indexes.append(track_idx)
        print("Playing track idx: ",track_idx)
        
        # now_playing = self.track_ids[track_idx]
        # artist = self.track_artists[track_idx]
        self.current_track_idx = track_idx

        track_to_play = self.track_ids[track_idx]
        if not testmode:
            print(f'\nNow playing: "{track_to_play}"\n')
        
            self.play_track(track_to_play, track_idx)
        return track_idx

