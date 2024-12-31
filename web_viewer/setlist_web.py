from flask import Flask, render_template, jsonify, request
import os, json

app = Flask(__name__)

run_on_host = os.environ.get('RUN_ON_HOST') 
using_port = os.environ.get('USING_PORT')
update_interval = os.environ.get('UPDATE_INTERVAL')
debug_mode = os.environ.get('DEBUG_MODE')

rows = []
setlist_data = []




print(f"run_on_host: {run_on_host}, Using Port: {using_port}, Update interval: {update_interval}, Debug: {debug_mode}")


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/load_setlist',methods=['POST'])
def load_setlist():
    global setlist_data

    # First, clear out the setlist in case there's already somethong there
    setlist_data.clear()

    json_string = request.get_json()
    setlist_data = json.loads(json_string)
    # Respond to the client
    return jsonify()


@app.route('/get_rows')
def get_rows():
    global setlist_data
    global get_rows
    
    rows.clear()
    # Example data generation: replace this with your actual logic
    # rows = [f"Row {i + 1}: " + "Some random text " + str(random.randint(1, 100)) for i in range(25)]
    for _ in range(len(setlist_data)):
        row_data = setlist_data[_]
        rows.append(f"{row_data['song_name']}, \
                      {row_data['artist_name']}, \
                      {row_data['album_name']}, \
                      {row_data['year_released']}")
    print(rows)
    x = jsonify(rows)
    return jsonify(rows)

if __name__ == '__main__':
    app.run(debug=True, threaded=True, port=using_port, host='0.0.0.0')
