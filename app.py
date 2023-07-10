from flask import Flask

app = Flask(__name__)
data_manager = JSONDataManager('movies.json')  # Use the appropriate path to your JSON file


@app.route('/')
def home():
    return "Welcome to MovieWeb App!"

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)