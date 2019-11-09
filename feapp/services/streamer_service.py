import feapp.data.db_session as db_session
from feapp.data.users import User
from feapp.data.userData import UserData
from feapp.data.userKeys import UserKeys
import feapp.data.userKeys as keyUtils
from passlib.handlers.sha2_crypt import sha512_crypt as crypto

streamer_db = {
    'frinkel': {
        'username': 'frinkel',
        'display': 'Holly Lotor',
        'tagline': 'A cool stream for cool people',
        'description': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam tempor, lacus vitae pellentesque '
                       'condimentum, est odio egestas mi, vel cursus dolor dui non libero. Sed pellentesque, enim quis '
                       'elementum maximus, felis mauris hendrerit magna, eget malesuada mauris eros ut risus. Aliquam '
                       'in dui non diam tristique porttitor. Nulla imperdiet ut nisi a dignissim. Suspendisse at '
                       'lacinia purus. Ut ut auctor tortor. Aenean vel elementum nunc. Morbi commodo nisi sit amet '
                       'erat pulvinar, id convallis risus porta. Sed id feugiat nulla. Nulla aliquam ornare erat, quis '
                       'lobortis nulla. Vestibulum faucibus felis at magna feugiat, ut varius tellus accumsan.',
        'avatar': '/static/uploads/avatar/frinkel.png',
        'background': '/static/img/glaceon-bg-blurred.png',
        'video-banner': '/static/img/glaceon-bg-blurred.png',
        'isStreaming': False,
        'streamingKey': '9EydmX7beJ8GxVbXgQv4zJrq8G5X7xyceq44bf5ReaSPVXVRCHWVxuWkQJxC7SaR'
    },
}


def get_streamer(user: str) -> UserData:
    if not user:
        return {}
    user = user.strip().lower()
    # streamer = streamer_db.get(user, {})
    session = db_session.create_session()
    return session.query(UserData).filter(UserData.username == user).first()
    # return streamer


def get_streamer_privdat(user: str) -> User:
    if not user:
        return {}
    user = user.strip().lower()
    # streamer = streamer_db.get(user, {})
    session = db_session.create_session()
    return session.query(User).filter(User.username == user).first()
    # return streamer


# A wrapper to get_streamer that returns nothing if the authkey doesn't match.
def authenticate_streamer(user: str, authkey: str) -> User:
    if not user:
        return {}
    session = db_session.create_session()
    streamer = session.query(UserKeys).filter(UserKeys.username == user).first()
    if not streamer:
        return {}
    if streamer.streamingKey == authkey:
        return streamer
    else:
        return {}


def markstarted(username: str):
    session = db_session.create_session()
    streamer = session.query(User).filter(User.username == username).first()
    streamer.is_streaming = True
    session.commit()


def markstopped(username: str):
    session = db_session.create_session()
    streamer = session.query(User).filter(User.username == username).first()
    streamer.is_streaming = False
    session.commit()


def changeKey(username: str) -> str:
    session = db_session.create_session()
    streamer = session.query(UserKeys).filter(UserKeys.username == username).first()
    streamer.streamingKey = keyUtils.genstreamkey()
    session.commit()
    return streamer.streamingKey


def changeTagline(username: str, tagline: str):
    session = db_session.create_session()
    streamer = session.query(UserData).filter(UserData.username == username).first()
    streamer.tagline = tagline
    session.commit()


def changeBackground(username: str, background: str):
    session = db_session.create_session()
    streamer = session.query(UserData).filter(UserData.username == username).first()
    # Set background to default if none is provided
    if background == '':
        background = '/static/img/glaceon-bg-blurred.png'
    streamer.background = background
    session.commit()
