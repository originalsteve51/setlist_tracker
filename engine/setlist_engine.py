import cmd
import requests
import json
import os

web_controller_url = os.environ['WEB_CONTROLLER_URL']
print('Web controller url: ', web_controller_url)


set_data = [{"song_name": "song 1", 
            "artist_name": "artist name 1",
            "album_name": "album 1",
            "year_released": "2009"},
            {"song_name": "song 2", 
            "artist_name": "artist name 2",
            "album_name": "album 2",
            "year_released": "1993"},
            {"song_name": "song 3", 
            "artist_name": "artist name 3",
            "album_name": "album 3",
            "year_released": "2012"}]


class CommandProcessor(cmd.Cmd):
    prompt = '(Using sample data)'
    def __init__(self):
        super(CommandProcessor, self).__init__()

    def do_webload(self, _):
        print(f'Loading set list data to web controller')

        requests.post(web_controller_url+'/load_setlist',
                            json=json.dumps(set_data))

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
