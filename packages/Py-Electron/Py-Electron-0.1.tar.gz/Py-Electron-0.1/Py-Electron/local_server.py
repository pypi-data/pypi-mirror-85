import flask, threading, sys, multiprocessing, os
from flask import request, jsonify, send_file

class local_server():

    def create(self, port, window_html):
        # ------------------------------ #
        # Initiates Flask server based on desired HTML.
        # Please note this is threaded. Need to investigate a way to properly kill server.
        # ------------------------------ #

        def _create(self, port, window_html):
            self.app = flask.Flask(__name__)

            @self.app.route('/', methods=['GET'])
            def home():
                return send_file(window_html)

            @self.app.route('/quit', methods=['GET'])
            def quit():
                # ------------------------------ #
                # This function is used to quit the Flask server. However it doesnt work
                # ------------------------------ #
                sys.exit()

            self.app.run(host='0.0.0.0', port=port)

        self.display_thread = multiprocessing.Process(target=_create, args=(self, port, window_html, ))
        self.display_thread.start()
