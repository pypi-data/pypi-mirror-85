from itertools import count

from squeezebox_cli.core.protocol import parse_tags
from squeezebox_cli.database import tracks


def pause_handler(status, msg, tn):
    if msg[1:3] == ['playlist', 'pause']:
        status['mode'] = 'pause' if msg[3] == '1' else 'play'
        return True
    return False


def play_handler(status, msg, tn):
    if msg[1] == 'play':
        status['mode'] = 'play'
        return True
    return False


def volume_handler(status, msg, tn):
    if msg[1:4] == ['prefset', 'server', 'volume']:
        status['volume'] = int(msg[4])
        return True
    return False


def newsong_handler(status, msg, tn):
    if msg[1:3] == ['playlist', 'newsong']:
        status['playlist_cur_index'] = int(msg[4])
        return True
    return False


def playlistcontrol_handler(status, msg, tn):
    if msg[1:3] == ['playlist', 'delete']:
        index = int(msg[3])
        del status['playlist'][index]
        if index < status['playlist_cur_index']:
            status['playlist_cur_index'] = status['playlist_cur_index'] - 1
        return True
    elif msg[1] == 'playlistcontrol':
        tags = dict(parse_tags(msg[2:]))
        try:
            ts = tracks(tn, track_id=int(tags['track_id']))
        except KeyError:
            try:
                ts = tracks(tn, album_id=int(tags['album_id']))
            except KeyError:
                ts = tracks(tn, artist_id=int(tags['artist_id']))

        def add():
            for t in ts:
                status['playlist'].append((t['id'], t['title']))

        def insert():
            for i, t in zip(count(status['playlist_cur_index'] + 1), ts):
                status['playlist'].insert(i, (t['id'], t['title']))

        def load():
            status['playlist'] = [(t['id'], t['title']) for t in ts]
            status['playlist_cur_index'] = 0
            status['mode'] = 'play'

        try:
            dict(add=add, insert=insert, load=load)[tags['cmd']]()
            return True
        except KeyError:
            print(tags)
    return False
