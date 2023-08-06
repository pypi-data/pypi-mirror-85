from datetime import timedelta
import dateparser

from squeezebox_cli.core.protocol import send_receive, parse_tags, \
        query_to_single_values, query_to_dicts


def rescan(tn):
    send_receive(tn, ['rescan'])


def rescanning(tn):
    return '1' == send_receive(tn, ['rescan', '?'])[1]


def rescan_playlists(tn):
    send_receive(tn, ['rescan', 'playlists'])


def rescan_progress(tn):
    tags = parse_tags(send_receive(tn, ['rescanprogress']))
    if tags[0] == ('rescan', '0'):
        return None
    importers = []
    response = dict(importers=importers)
    for k, v in tags[1:]:
        if k == 'totaltime':
            h, m, s = v.split(':')
            response[k] = timedelta(
                    hours=int(h), minutes=int(m), seconds=int(s))
        else:
            importers.append((k, int(v)))
    return response


def total_genres(tn):
    return int(send_receive(tn, ['info', 'total', 'genres', '?'])[3])


def total_artists(tn):
    return int(send_receive(tn, ['info', 'total', 'artists', '?'])[3])


def total_albums(tn):
    return int(send_receive(tn, ['info', 'total', 'albums', '?'])[3])


def total_songs(tn):
    return int(send_receive(tn, ['info', 'total', 'songs', '?'])[3])


def query_args(search, artist_id, album_id, track_id, genre_id):
    args = []
    if search:
        args.append(f'search:{search}')
    if artist_id:
        args.append(f'artist_id:{artist_id}')
    if album_id:
        args.append(f'album_id:{album_id}')
    if track_id:
        args.append(f'track_id:{track_id}')
    if genre_id:
        args.append(f'genre_id:{genre_id}')
    return args


def genres(
        tn, search=None, artist_id=None, album_id=None, track_id=None,
        genre_id=None):
    return query_to_single_values(
            tn, 'genres', 50, 'id', 'genre',
            query_args(search, artist_id, album_id, track_id, genre_id))


def artists(
        tn, search=None, artist_id=None, album_id=None, track_id=None,
        genre_id=None):
    return query_to_single_values(
            tn, 'artists', 100, 'id', 'artist',
            query_args(search, artist_id, album_id, track_id, genre_id))


def albums(
        tn, search=None, artist_id=None, album_id=None, track_id=None,
        genre_id=None, year=None, compilation=None, sort=None,
        extended=False):
    args = query_args(search, artist_id, album_id, track_id, genre_id)
    if year is not None:
        args.append(f'year:{year}')
    if compilation is not None:
        args.append(f'compilation:{1 if compilation else 0}')
    if sort is not None:
        args.append(f'sort:{sort}')
    if extended:
        return query_to_dicts(
                tn, 'albums', 100, 'id', ['tags:ywaSsXl'] + args,
                dict(
                    id=int,
                    year=lambda v: None if v == '0' else int(v),
                    compilation=lambda v: v == '1',
                    album=lambda v: v,
                    album_replay_gain=lambda v: float(v),
                    artist_id=lambda v: int(v),
                    artist=lambda v: v,
                    textkey=lambda v: v,
                ))
    return query_to_single_values(tn, 'albums', 100, 'id', 'album', args)


def years(tn):
    start = 0
    chunk_size = 100
    count = None
    ys = []
    while count is None or len(ys) < count:
        for k, v in parse_tags(
                send_receive(tn, ['years', f'{start}', f'{chunk_size}'])):
            if k == 'year':
                ys.append(int(v))
            elif k == 'count':
                count = int(v)
        start += chunk_size
    return ys


def songinfo(tn, track_id):
    tag_handlers = dict(
            id=int,
            duration=float,
            album_id=int,
            year=int,
            tracknum=int,
            samplesize=int,
            samplerate=int,
            replay_gain=float,
            genre_id=int,
            filesize=int,
            artist_id=int,
            album_replay_gain=float,
            channels=int,
            compilation=lambda v: v == '1',
            coverart=lambda v: v == '1',
            modificationTime=dateparser.parse,
            lastUpdated=dateparser.parse,
            addedTime=dateparser.parse,
        )
    info = dict()
    for k, v in parse_tags(
            send_receive(
                tn,
                ['songinfo', '0', '100', f'track_id:{track_id}',
                    'tags:aCdegilpqstuy']))[2:]:
        try:
            info[k] = tag_handlers[k](v)
        except KeyError:
            info[k] = v
    return info


def tracks(
        tn, search=None, artist_id=None, album_id=None, track_id=None,
        genre_id=None, year=None, sort=None, extended=False):
    args = query_args(search, artist_id, album_id, track_id, genre_id)
    if extended:
        args.append('tags:ytsplgedCa')
    if album_id or artist_id:
        args.append('sort:albumtrack')
    return query_to_dicts(tn, 'tracks', 100, 'id', args, tag_handlers=dict(
        id=int,
        duration=float,
        album_id=int,
        artist_id=int,
        genre_id=int,
        tracknum=int,
        year=int,
        compilation=lambda v: v == '1'))


def search(tn, term):
    count = None
    start = 0
    chunk_size = 5
    results = dict(artists=dict(), tracks=dict(), albums=dict())
    while (count is None or
            len(results['artists']) + len(results['tracks']) +
            len(results['albums']) < count):
        tags = parse_tags(
                send_receive(
                    tn,
                    ['search', f'{start}', f'{chunk_size}', f'term:{term}']))
        while tags:
            k, v = tags.pop(0)
            if k == 'contributor_id':
                k2, artist = tags.pop(0)
                results['artists'][int(v)] = artist
            elif k == 'track_id':
                k2, track = tags.pop(0)
                results['tracks'][int(v)] = track
            elif k == 'album_id':
                k2, album = tags.pop(0)
                results['albums'][int(v)] = album
            elif k == 'count':
                count = int(v)
        start += chunk_size
    return results
