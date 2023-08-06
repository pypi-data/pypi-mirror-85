import asyncio
import logging
import threading
from aiortc import RTCPeerConnection, RTCSessionDescription
from aiortc.contrib.media import MediaPlayer
from grpc.experimental import aio
from webrtc_streaming.autogen import (
    webrtc_streaming_pb2_grpc as pb2_grpc
)
from webrtc_streaming.autogen import (
    webrtc_streaming_pb2 as webrtc_streaming_pb2_pb2
)
from webrtc_streaming.remote import start as communicate_with_signaling_server


class WebRTC_Streaming_Service(pb2_grpc.WebRTC_StreamingServicer):
    def __init__(self, rtp_video_port):
        self.pcs = set()
        self.rtp_video_port = rtp_video_port

    async def Negotiate(self, request, context):
        message = request
        sdp = message.sdp
        type_ = message.type

        offer = RTCSessionDescription(sdp=sdp, type=type_)

        pc = RTCPeerConnection()
        self.pcs.add(pc)

        @pc.on("iceconnectionstatechange")
        async def on_iceconnectionstatechange():
            print("ICE connection state is %s" % pc.iceConnectionState)
            if pc.iceConnectionState == "failed":
                await pc.close()
                self.pcs.discard(pc)

        f = open("/tmp/webrtc_streaming.sdp", "w+")
        sdp = "c=IN IP4 0.0.0.0\n"
        sdp += "m=video %s RTP/AVP 96\n" % self.rtp_video_port
        sdp += "a=rtpmap:96 H264/90000"

        f.write(sdp)
        f.close()

        options = {"protocol_whitelist": "file,rtp,udp",
                   "buffer_size": "20000000"}
        player = MediaPlayer("/tmp/webrtc_streaming.sdp", options=options)

        await pc.setRemoteDescription(offer)
        for t in pc.getTransceivers():
            if t.kind == "audio" and player.audio:
                pc.addTrack(player.audio)
            elif t.kind == "video" and player.video:
                pc.addTrack(player.video)

        answer = await pc.createAnswer()
        await pc.setLocalDescription(answer)
        response = webrtc_streaming_pb2_pb2.SDP(
            sdp=pc.localDescription.sdp, type=pc.localDescription.type)
        return response


async def _start_async_server(rtp_video_port):
    server = aio.server()
    server.add_insecure_port("[::]:50051")
    pb2_grpc.add_WebRTC_StreamingServicer_to_server(
        WebRTC_Streaming_Service(rtp_video_port), server
    )
    await server.start()
    await server.wait_for_termination()


def run_webrtc_service(rtp_video_port):
    logging.basicConfig()
    loop = asyncio.get_event_loop()
    loop.create_task(_start_async_server(rtp_video_port))
    loop.run_forever()


def start(signaling_server, secret_key, rtp_video_port):
    args = [signaling_server, secret_key]
    t = threading.Thread(
        target=communicate_with_signaling_server, args=args)
    t.start()
    run_webrtc_service(rtp_video_port)
