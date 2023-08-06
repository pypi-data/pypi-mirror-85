# https://github.com/aslushnikov/getting-started-with-cdp
# from websocketcontrols import evaluate_target_created
import json, websocket

class WebsocketConnection():

    def __init__(self, port):
        try:
            import thread
        except ImportError:
            import _thread as thread

        import time

        def on_message(ws, message):
            message = json.loads(message)
            print("==========")
            print(message)
            try:
                print(message["method"])
                if message["method"] == "Target.targetCreated":
                    if message["params"]["targetInfo"]["type"] == "page":
                        self.target_id = message["params"]["targetInfo"]["targetId"]
                        print("Identified Target ID " +  self.target_id)

                    set_payload = json.dumps({
                        "id": 2,
                        'method': 'Target.attachToTarget',
                        'params': {
                            'targetId': self.target_id,
                            'flatten': True
                        },
                    }, separators=(',', ':'))
                    ws.send(set_payload)

                elif message["method"] == "Target.attachedToTarget":
                    print("I'm attached :0")
                    self.session_id = message["params"]["sessionId"]
                    print("Set Session ID " + self.session_id)

                    set_payload = json.dumps({
                        'sessionId': self.session_id,
                        'id': 2,
                        'method': 'Page.navigate',
                        'params': {
                            'url': self.intended_url
                        },
                    }, separators=(',', ':'))
                    ws.send(set_payload)

            except KeyError:
                pass

        def on_error(ws, error):
            print(error)

        def on_close(ws):
            print("### closed ###")

        self.on_message = on_message
        self.on_error = on_error
        self.on_close = on_close

    def go_to_url(self, url):
        self.intended_url = url
        available_targets_payload = json.dumps({
            "id": 1,
            'method': 'Target.setDiscoverTargets',
            'params': {
              'discover': True
            },
        }, separators=(',', ':'))
        ws.send(available_targets_payload)

    def connect(self, _ws):
        print("Connecting to ws on " + _ws)


        def on_open(ws):
            pass

        self.on_open = on_open
        websocket.enableTrace(True)
        self.ws = websocket.WebSocketApp(_ws,
                                  on_message = self.on_message,
                                  on_error = self.on_error,
                                  on_close = self.on_close)
        self.ws.on_open = self.on_open
        self.ws.run_forever()
