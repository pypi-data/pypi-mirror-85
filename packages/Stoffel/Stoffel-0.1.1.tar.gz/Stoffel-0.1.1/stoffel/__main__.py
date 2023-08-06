import webbrowser
from stoffel.app import app

def main():
    url = "http://localhost:5500"
    webbrowser.open_new(url)
    app.run(port=5500, debug=False)
