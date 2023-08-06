from squeezebox_cli.core.protocol import send_receive, parse_tags, \
        chunked_query, query_to_dicts, receive


def int_tag_handler(d, k, v):
    d[k] = int(v)


def str_tag_handler(d, k, v):
    d[k] = v.rstrip()


def float_tag_handler(d, k, v):
    d[k] = float(v)


def bool_tag_handler(d, k, v):
    d[k] = v == '1'


player_status_tag_handlers = {
        'playlist shuffle': (
            lambda d, k, v: bool_tag_handler(d, 'shuffle', v)),
        'playlist repeat': (lambda d, k, v: bool_tag_handler(d, 'repeat', v)),
        'mode': str_tag_handler,
        'player_name': (lambda d, k, v: str_tag_handler(d, 'name', v)),
        'playlist_cur_index': int_tag_handler,
        'duration': float_tag_handler,
        'mixer volume': (lambda d, k, v: int_tag_handler(d, 'volume', v)),
    }

#
# public interface
#


def id_from_index_or_name(tn, player_index_or_name):
    players = list_all(tn)
    try:
        try:
            return players[int(player_index_or_name)]['playerid']
        except ValueError:
            return[p for p in players
                   if p['name'] == player_index_or_name][0]['playerid']
    except IndexError:
        return None


def list_all(tn):
    return query_to_dicts(tn, 'players', 100, 'playerindex', [], dict(
            isplaying=lambda v: v == '1',
            name=str,
            playerid=str,
            playerindex=int,
        ), strict=True)


def stop(tn, player_id):
    send_receive(tn, [player_id, 'stop'])


def play(tn, player_id, track_id=None, album_id=None):
    id = None
    if track_id:
        id = f'track_id:{track_id}'
    elif album_id:
        id = f'album_id:{album_id}'
    if id:
        send_receive(tn, [player_id, 'playlistcontrol', 'cmd:load', id])
    else:
        send_receive(tn, [player_id, 'play'])


def pause(tn, player_id):
    send_receive(tn, [player_id, 'pause'])


def next(tn, player_id):
    send_receive(tn, [player_id, 'playlist', 'index', '+1'])


def previous(tn, player_id):
    send_receive(tn, [player_id, 'playlist', 'index', '-1'])


def status(tn, player_id):
    results = dict(playlist=[])
    track_count = None
    start = 0
    chunk_size = 100
    while track_count is None or len(results['playlist']) < track_count:
        reply = send_receive(
                tn, [player_id, 'status', f'{start}', f'{chunk_size}'])
        results['playerid'] = reply[0]
        tags = parse_tags(reply)
        while tags:
            k, v = tags.pop(0)
            if k == 'playlist index':
                # take next 2 and add to playlist
                ktid, vtid = tags.pop(0)
                ktitle, vtitle = tags.pop(0)
                results['playlist'].append((int(vtid), vtitle))
            elif k == 'playlist_tracks':
                track_count = int(v)
            else:
                try:
                    player_status_tag_handlers[k](results, k, v)
                except KeyError:
                    # ignore unhandled tags
                    pass
        start += chunk_size
        if track_count is None:
            break
    return results


def count(tn):
    return int(send_receive(tn, ['player', 'count', '?'])[2])


def indexed_simple(tn, cmd, index):
    return send_receive(tn, ['player', cmd, f'{index}', '?'])[3]


def id(tn, index):
    return indexed_simple(tn, 'id', index)


def name(tn, index):
    return indexed_simple(tn, 'name', index)


def ip(tn, index):
    return indexed_simple(tn, 'ip', index)


def signal_strength(tn, id):
    return int(send_receive(tn, [id, 'signalstrength', '?'])[2])


def connected(tn, id):
    return send_receive(tn, [id, 'connected', '?'])[2] == '1'


def synced_to(tn, id):
    ids = send_receive(tn, [id, 'sync', '?'])[2]
    return [] if ids == '-' else ids.split(',')


def sync_to(tn, sync_to_id, to_sync_id):
    send_receive(tn, [sync_to_id, 'sync', f'{to_sync_id}'])


def sync_groups(tn):
    tags = dict(parse_tags(send_receive(tn, ['syncgroups', '?'])))
    if tags:
        return list(zip(
            tags['sync_members'].split(','),
            tags['sync_member_names'].split(',')))
    else:
        return []


def get_volume(tn, id):
    return int(send_receive(tn, [id, 'mixer', 'volume', '?'])[3])


def set_volume(tn, id, vol):
    send_receive(tn, [id, 'mixer', 'volume', f'{vol}'])


def change_volume(tn, id, step, up=True):
    send_receive(tn, [id, 'mixer', 'volume', f'+{step}' if up else f'-{step}'])


def mute(tn, id):
    send_receive(tn, [id, 'mixer', 'muting', '1'])


def unmute(tn, id):
    send_receive(tn, [id, 'mixer', 'muting', '0'])


def toggle_mute(tn, id):
    send_receive(tn, [id, 'mixer', 'muting'])


def get_mute(tn, id):
    return send_receive(tn, [id, 'mixer', 'muting', '?'])[3] == '1'


def players(tn):
    tag_handlers = dict(
            playerid=(lambda d, k, v: str_tag_handler(d, 'id', v)),
            connected=(lambda d, k, v: bool_tag_handler(d, k, v)),
        )
    tag_groups = chunked_query(tn, 'players', 5, 'playerindex')
    ps = []
    for tg in tag_groups:
        for k, v in tg:
            if k == 'playerindex':
                ps.append(dict(index=int(v)))
            elif k == 'count':
                pass
            else:
                try:
                    tag_handlers[k](ps[-1], k, v)
                except KeyError:
                    ps[-1][k] = v
    return ps


def playlist_add(tn, player_id, track_id=None, album_id=None, artist_id=None):
    if track_id:
        id = f'track_id:{track_id}'
    elif album_id:
        id = f'album_id:{album_id}'
    elif artist_id:
        id = f'artist_id:{artist_id}'
    send_receive(tn, [player_id, 'playlistcontrol', 'cmd:add', id])


def listen(tn, playerid=None, commands=None):
    send_receive(tn, ['listen', '1'])
    while True:
        n = receive(tn)
        if (playerid is None or n[0] == playerid) and \
                (commands is None or n[1] in commands):
            yield n


def playlist_remove(tn, player_id, index):
    send_receive(tn, [player_id, 'playlist', 'delete', f'{index}'])
