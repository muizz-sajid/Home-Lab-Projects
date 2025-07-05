import pychromecast
from core.protocols import Device
import re
import yt_dlp
from pychromecast.controllers.youtube import YouTubeController
import logging

class ChromecastDevice(Device):
    def __init__(self, chromecast):
        self.name = chromecast.name
        self._casts = chromecast

    @classmethod
    def discover(cls):
        
        chromecasts, browser = pychromecast.get_chromecasts(timeout=15)

        devices = []
        for cast in chromecasts:
            cast.wait() 
            devices.append(cls(cast))

        return devices
        

    def _ensure_connected(self):
        if self._casts is None:
            raise RuntimeError("Chromecast is not connected or initialized.")
        

    def turn_on(self):
        self._ensure_connected()
        self._casts.start_app("YouTube")
        self._casts.quit_app()


    def turn_off(self):
        self._ensure_connected()
        self._casts.quit_app()


    def play_media(self, url):
        self._ensure_connected()
        media = self._casts.media_controller
        media.play_media(url, "video/mp4")
        media.block_until_active()


    def launch_youtube(self):
        try:
            self._ensure_connected()
            self._casts.start_app("YouTube")
        except pychromecast.error.RequestFailed as e:
                logging.error(f"[ChromecastDevice] Failed to launch YouTube: {e}")
                return False
        

    def play_youtube(self, query_or_url: str):

        self._ensure_connected()

        try:
            url_match = re.search(r"(?:v=|youtu\.be/)([\w-]{11})", query_or_url)
            if url_match:
                video_id = url_match.group(1)
                print(f"[YouTube] Detected ID directly: {video_id}")
            else:

                print(f"[YouTube] Searching for: {query_or_url}")
                ydl_options = { 
                    "quiet": True,
                    "skip_download": True,
                    "format": "best",
                    "default_search": "ytsearch1",
                }
                with yt_dlp.YoutubeDL(ydl_options) as ydl:
                    info = ydl.extract_info(query_or_url)
                    entry = info["entries"][0]
                    video_id = entry["id"]
                    print(f"[YouTube] Search result ID: {video_id}")

            yt = YouTubeController()
            self._casts.register_handler(yt)
            print(f"[YouTube] Launching video ID: {video_id}")
            yt.play_video(video_id)

        except Exception as e:
            print(f"[YouTube] Error while trying to cast: {e}")


    def launch_netflix(self):
        try:
            self._casts.start_app("CA5E8412")
            return True
        except pychromecast.error.RequestFailed as e:
            logging.error(f"[ChromecastDevice] Failed to launch Netflix: {e}")
            return False


    def launch_spotify(self):
        try:
            self._casts.start_app("CC32E753")
            return True
        except pychromecast.error.RequestFailed as e:
            logging.error(f"[ChromecastDevice] Failed to launch Spotify: {e}")
            return False


    def volume(self, lvl):
        self._ensure_connected()
        self._casts.set_volume(lvl)


    def volume_up(self):
        self._ensure_connected()
        current = self._casts.status.volume_level
        self._casts.set_volume(min(current + 0.05, 1.0))


    def volume_down(self):
        self._ensure_connected()
        current = self._casts.status.volume_level
        self._casts.set_volume(max(current - 0.05, 0.0))


    def mute(self):
        self._ensure_connected()
        self._casts.set_volume_muted(True)


    def unmute(self):
        self._ensure_connected()
        self._casts.set_volume_muted(False)


    def playback(self, action):
        self._ensure_connected()
        media = self._casts.media_controller
        action = action.lower()

        if action == "play":
            media.play()
        elif action == "pause":
            media.pause()
        elif action == "stop":
            media.stop()
        elif action.startswith("seek:"):
            try:
                secs = float(action.split(":", 1)[1])
                media.seek(secs)
            except ValueError:
                print("Invalid Seek Time")
        else:
            print(f"Unknown Action: {action}")


    def get_status(self):
        self._ensure_connected()
        status = self._casts.status  

        # 1) Try old-style player_state
        ps = getattr(status, "player_state", None)
        if ps is not None:
            is_active = ps not in ("IDLE", "UNKNOWN")

        else:
            # 2) Try newer transport_state
            ts = getattr(status, "transport_state", None)
            if ts is not None:
                is_active = ts not in ("IDLE", "UNKNOWN")
            else:
                # 3) Ultimate fallback: if there's any display_name, assume active
                is_active = bool((getattr(status, "display_name", "") or "").strip())

        return {
            
            "volume":    getattr(status, "volume_level", None),
        }
        