import flask

from feapp.infrastructure.view_modifiers import response
from feapp.infrastructure import request_dict
import feapp.services.streamer_service as streamer_service
from feapp.data.userData import UserData

blueprint = flask.Blueprint('stream', __name__, template_folder='templates')


@blueprint.route('/stream/<string:streamer>')
@response(template_file='stream/both.html')
def streamPage(streamer: str):
    print("Fetching stream details for {}".format(streamer))

    streamer = streamer_service.get_streamer(streamer)
    stream_pri = streamer_service.get_streamer_privdat(streamer.username)
    if not streamer:
        return flask.abort(404)

    return {
        'username': streamer.username,
        'displayName': streamer.displayName,
        'background': streamer.background,
        'isStreaming': stream_pri.is_streaming,
        'tagline': streamer.tagline,
        'description': streamer.description,
        'avatar': streamer.avatar,
    }


@blueprint.route('/<string:streamer>.js')
@response(mimetype="text/javascript")
def streamerOptions(streamer: str):
    streamer = streamer_service.get_streamer(streamer)
    if not streamer:
        return flask.abort(404)
    return 'video.poster = "{}"'.format(streamer.videoBanner)


@blueprint.route('/hls/<string:streamer>.m3u8')
@response(template_file='stream/streamer.m3u8', mimetype='application/vnd.apple.mpegurl')
def genm3u8(streamer: str):
    streamer = streamer_service.get_streamer(streamer)
    if not streamer:
        return flask.abort(404)
    return {
        'username': streamer.username
    }


# Config Sample for OBS:
# Streaming URL: rtmp://glaceon.live/broadcast/foo
# Stream Key: <auth key here>
# Config Sample for nginx_rtmp in the user's config:
# on_publish http://glaceon.live/startstream/foo;
# Authentication URL:
# http://glaceon.live/startstream/foo?name=<auth key here>
@blueprint.route('/startstream/<string:streamer>', methods=['POST'])
def startstream(streamer: str):
    data = request_dict.create(default_val='')
    authkey = data.name.strip()
    streamer = streamer_service.authenticate_streamer(streamer, authkey)
    if not streamer:
        return flask.abort(404)
    else:
        streamer_service.markstarted(streamer.username)
        return flask.Response("", status=201)


# Same as above but with on_publish_done instead of on_publish.
# It doesn't actually check for the status code at the end, but eh.
# The big deal about this function is that it'll update front-end values.
@blueprint.route('/stopstream/<string:streamer>', methods=['POST'])
def endstream(streamer: str):
    data = request_dict.create(default_val='')
    authkey = data.name.strip()
    streamer = streamer_service.authenticate_streamer(streamer, authkey)
    if not streamer:
        return flask.abort(404)
    else:
        streamer_service.markstopped(streamer.username)
        return flask.Response("", status=201)


@blueprint.route('/api/v1/changekey/<string:streamer>', methods=['POST'])
def streamKeyChangeRoute(streamer: str):
    data = request_dict.create(default_val='')
    authkey = data.name.strip()
    streamer = streamer_service.authenticate_streamer(streamer, authkey)
    if not streamer:
        return flask.abort(404)
    else:
        newkey = streamer_service.changeKey(streamer.username)
        return flask.Response('{}'.format(newkey), status=200)


@blueprint.route('/api/v1/changetagline/<string:streamer>', methods=['POST'])
def taglineChangeRoute(streamer: str):
    data = request_dict.create(default_val='')
    authkey = data.name.strip()
    tagline = data.tagline.strip()
    streamer = streamer_service.authenticate_streamer(streamer, authkey)
    if not streamer:
        return flask.abort(404)
    else:
        streamer_service.changeTagline(streamer.username, tagline)
        return flask.Response("", status=200)
      

@blueprint.route('/api/v1/changebackground/<string:streamer>', methods=['POST'])
def backgroundChangeRoute(streamer: str):
    # TODO: Implement a way to upload a background through this API endpoint.
    data = request_dict.create(default_val='')
    authkey = data.name.strip()
    bg = data.bg.strip()
    streamer = streamer_service.authenticate_streamer(streamer, authkey)
    if not streamer:
        return flask.abort(404)
    else:
        streamer_service.changeBackground(streamer.username, bg)
        return flask.Response("Changed background to {}".format(bg), status=200)
