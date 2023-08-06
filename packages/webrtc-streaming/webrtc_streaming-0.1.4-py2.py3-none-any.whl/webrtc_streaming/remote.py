import socketio
from webrtc_streaming.negotiate import negotiate


def start(signalig_server, secret_key):
    sio = socketio.Client()

    @sio.event
    def connect():
        print("Connected to server %s" % signalig_server)
        sio.emit("create_room", secret_key)

    @sio.event
    def viewer_need_offer(data):
        viewer_id = data["viewer_id"]
        remote_description = data["offer"]
        print("Server ask for offer to viewer " + viewer_id)
        sdp = remote_description["sdp"]
        type_ = remote_description["type"]
        answer = negotiate(
            "localhost:50051", sdp, type_)
        sio.emit("offer_to_viewer", {"viewer_id": viewer_id, "offer": answer})

    @sio.event
    def disconnect():
        print('Disconnected from server')

    sio.connect(signalig_server)
    sio.wait()
