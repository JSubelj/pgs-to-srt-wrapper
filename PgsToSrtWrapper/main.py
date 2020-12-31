import ffmpeg
import discovery
import conversion

print("Starting watching for new qbittorrent file",flush=True)
discovery.watch_for_qbittorrent_notifications(conversion.get_eng_subtitles)

