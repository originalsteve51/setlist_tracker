
import spotipy



#-------------------------------------------------------------------
# Player class
#-------------------------------------------------------------------
class Player():
    def __init__(self, sp):
        self.active_player = None
        self.sp = sp
        self.unplayed_tracks = set()
        self.paused = False
        

    def show_available_players(self, list_all_players=True):
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

    def play_track(self, track_id):
        try:
            # Set the repeat mode to off, otherwise the track will repeat
            # and this is not what I think we want. Tracks should just
            # play once for MINGO
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
        self.paused = True

    def play_next_track(self, testmode=False):
        if len(self.unplayed_tracks) == 0:
            print('All tracks have been played.')
            return

        track_idx = random.choice(self.unplayed_tracks)
        self.unplayed_tracks.remove(track_idx)
        self.played_tracks.append(track_idx)
        print("Playing track idx: ",track_idx)
        
        now_playing = self.track_info[track_idx]
        artist = self.track_artists[track_idx]
        self.current_track_idx = track_idx
        self.game_monitor.add_to_played_tracks(now_playing)

        print(f'\nNow playing: "{now_playing}" by "{artist}"\n')
        track_to_play = self.track_ids[track_idx]
        if not testmode:
            self.player.play_track(track_to_play)

