from .commands import list_all, stop, play, status, id_from_index_or_name, \
        next, previous, pause
from .commands import count, id, name, ip, signal_strength, connected, \
        synced_to, sync_to, sync_groups, get_volume, set_volume, \
        change_volume, mute, unmute, toggle_mute, get_mute, players, \
        listen, playlist_add, playlist_remove
from .notifications import pause_handler, volume_handler, newsong_handler, \
        playlistcontrol_handler, play_handler

notification_handlers = [
        pause_handler, volume_handler, newsong_handler,
        playlistcontrol_handler, play_handler]
