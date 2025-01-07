from flask import Flask, render_template, jsonify, request
import os, json

app = Flask(__name__)

run_on_host = os.environ.get('RUN_ON_HOST') 
using_port = os.environ.get('USING_PORT')
update_interval = os.environ.get('UPDATE_INTERVAL')
debug_mode = os.environ.get('DEBUG_MODE')

# Global data that is set from the engine and later provided
# to the view page
rows = []
setlist_data = []
songs_info = []
playlist_name='My Playlist'

print(f"run_on_host: {run_on_host}, Using Port: {using_port}, Update interval: {update_interval}, Debug: {debug_mode}")

"""
Display the index.html page, which is used to view a set list whose
contents were previously posted here from the engine.
"""
@app.route('/')
def home():
    global playlist_name
    return render_template('index.html', playlist_name=playlist_name)

"""
The set list is prepared by the engine and posted here as a list of JSON
rows containing info about songs.
"""
@app.route('/load_setlist',methods=['POST'])
def load_setlist():
    global setlist_data
    global songs_info

    # First, clear out the setlist and info in case there's already something there
    setlist_data.clear()
    songs_info.clear()

    # Data posted here by the engine is saved in global data for retrieval
    # by requests issued to /get_rows from a web page wanting to view the set list
    json_string = request.get_json()
    setlist_data = json.loads(json_string)

    for _ in range(0, len(setlist_data)):
        songs_info.append({'info': setlist_data[_]['song_info'], 'name': setlist_data[_]['song_name'] })
        print(songs_info[_]['name'])
    
    # Respond to the client with an OK status (jsonify with no args does this)
    return jsonify()

@app.route('/get_song_info', methods=['GET'])
def get_song_info():
    song_number = int(request.args.get('song_number')) 
    song_name = songs_info[song_number]['name']
    return render_template('info.html', song_name=song_name, song_number=song_number)

@app.route('/song_info', methods=['GET'])
def song_info():
    song_number = request.args.get('song_number') 
    song_info = songs_info[int(song_number)] 
    return jsonify(song_info)   

@app.route('/playlist_info', methods=['POST'])
def playlist_info():
    global playlist_name
    json_string = request.get_json()
    playlist_data = json.loads(json_string)
    playlist_name = playlist_data['name']

    return jsonify()


"""
The index page calls /get_rows to obtain the set list data.
"""
@app.route('/get_rows',methods=['GET'])
def get_rows():
    global setlist_data
    global rows
    global songs_info

    # Get a clean start!
    rows.clear()

    # Build the list of rows from the JSON data provided by the engine.
    # Each row is just a string with song information that will be shown
    # on the index page.
    for _ in range(len(setlist_data)):
        row_data = setlist_data[_]
        # print(row_data)
        a_row = list()
        a_row.append(f"{row_data['song_name']}")
        a_row.append(f"{row_data['artist_name']}")
        a_row.append(f"{row_data['album_name']}")
        a_row.append(f"{row_data['year_released']}")


        rows.append(a_row)

        #rows = [[f"Row {i + 1} Col {j + 1}" for j in range(4)] for i in range(25)]

        # print(rows)

        """
        rows.append(f"{row_data['song_name']}, \
                      {row_data['artist_name']}, \
                      {row_data['album_name']}, \
                      {row_data['year_released']}")
        """
    
    # Return the list in JSON form for the page to render.
    return jsonify(rows)

if __name__ == '__main__':
    app.run(debug=True, threaded=True, port=using_port, host='0.0.0.0')
