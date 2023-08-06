from locate_chrome import get_path
from subprocess import Popen, PIPE
from local_server import local_server
from default_args import get_args, transform_args
from requests_futures.sessions import FuturesSession
import requests, os, time
from websockets import WebsocketConnection

class Application():
    def __init__(self, *args, **kwargs):
        self.debug = False
        for arg in kwargs:
            if arg == "debug":
                self.debug = kwargs[arg]

    def quit(self):
        # ------------------------------ #
        # Exits from all windows.
        # ------------------------------ #
        for window in self.array:
            window.exit()

    class Window():
        def __init__(self):
            # ------------------------------ #
            # Initializes args.
            # ------------------------------ #
            self.width = 1040
            self.height = 1080
            self.launch_as_app = True
            self.html = ''
            self.no_gpu = True
            self.dark_mode = False

        def exit():
            # ------------------------------ #
            # Kills the Chrome window.
            # ------------------------------ #
            self.process.terminate()

        def create(self, *args, **kwargs):
            # ------------------------------ #
            # Launches Google Chrome and navigates to Flask server.
            # ------------------------------ #

            for arg in kwargs:
                if arg == "height":
                    self.height = kwargs[arg]
                elif arg == "width":
                    self.width = kwargs[arg]
                elif arg == "html":
                    self.html = kwargs[arg]
                elif arg == "src":
                    with open(kwargs[arg], 'r') as f:
                         self.html = f.read()
                elif arg == "dark_mode":
                    self.dark_mode = kwargs[arg]

            local_server().create(8081, self.html)
            args = transform_args(self, [get_path(),
                    '--app=http://localhost:8081',
                    '--remote-debugging-port=8888',
                    '--no-first-run'
                    '--user-data-dir=' + os.path.join(os.path.dirname(__file__), 'user_dir/')
                ] + get_args())

            self.process = Popen(args, shell=False, stdin=PIPE, stdout=PIPE, bufsize=1)

            while True:
                try:
                    # ------------------------------ #
                    # Attempt to fetch browser data
                    # ------------------------------ #
                    _browser_data = requests.get("http://127.0.0.1:8888/json/version").json()
                    self.v8_version = _browser_data['V8-Version']
                    self.webkit_version = _browser_data['WebKit-Version']
                    self.tls_protocol = _browser_data['Protocol-Version']
                    self._ws = _browser_data['webSocketDebuggerUrl']
                    print("Grabbed browser data")
                    print(vars(self))
                    break
                except:
                    print("Error grabbing browser data, retrying")
                    time.sleep(1)

            print("Waiting to connect... (1s delay)")
            time.sleep(1)
            self._conn = WebsocketConnection('8888')
            self._conn.connect(self._ws)

if __name__ == "__main__":
    Application(debug=True).Window().create(html="./static/index.html", dark_mode=True)
