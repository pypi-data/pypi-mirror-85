import grpc
from webrtc_streaming.autogen import (
    webrtc_streaming_pb2 as webrtc_streaming_pb2
)
from webrtc_streaming.autogen import (
    webrtc_streaming_pb2_grpc as webrtc_streaming_pb2_grpc
)


def negotiate(ip_server, sdp, type_):
    sdp = webrtc_streaming_pb2.SDP(sdp=sdp, type=type_)
    channel = grpc.insecure_channel(ip_server)
    stub = webrtc_streaming_pb2_grpc.WebRTC_StreamingStub(channel)
    response = stub.Negotiate(sdp)
    return {"sdp": response.sdp, "type": response.type}
