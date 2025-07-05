import time
import numpy as n
from threading import Thread

try:
    import sounddevice as sd
    HAS_SOUNDDEVICE = True
except OSError:
    HAS_SOUNDDEVICE = False
    print("ClapDetector: sounddevice/PortAudio not available; clap detection disabled.")

class ClapDetector:
    def __init__(self, callback, threshold = 20.0, decay_thresh = 3.0, cooldown = 1.0, clap_window = 0.6, max_duration = 0.4):
        self.callback = callback
        self.threshold = threshold
        self.decay_thresh = decay_thresh
        self.max_duration = max_duration
        self.cooldown = cooldown
        self.clap_window = clap_window

        self.last_clap_time = 0.0
        self.clap_count = 0
        self.running = False
        self.last_trigger = 0.0
        self.in_transient = False

        self.stream = None
        self.thread = None


    def _audio_callback(self, indata, frames, time_info, status):
        if status:
            print(f"[ClapDetector] Stream Status: {status}")

        volume = n.linalg.norm(indata) * 10
        now = time.time()

        if not self.in_transient:
            if volume > self.threshold:
                print(f"[ClapDetector] Volume: {volume:.3f}")
                self.in_transient = True
                self.trans_start = now
            return
        
        if volume > self.decay_thresh:
            return
        
        dur = now - self.trans_start
        self.in_transient = False
        print(f"[ClapDetector] Transient dur={dur:.3f}s")

        if dur <= self.max_duration:
            if now - self.last_clap_time > self.clap_window:
                self.clap_count = 0

            if now - self.last_trigger > self.cooldown:
                self.clap_count = self.clap_count + 1
            else:
                self.clap_count = 1

            self.last_clap_time = now
            print(f"[ClapDetector] clap_count={self.clap_count}")

            if self.clap_count == 2 and now - self.last_trigger > self.cooldown:
                print("[ClapDetector] double‑clap detected!")
                self.last_trigger = now
                Thread(target=self.callback, daemon=True).start()
                self.clap_count = 0
        else:
            print("[ClapDetector] Ignored: transient too long")

        return


    def start(self):
            if not HAS_SOUNDDEVICE:
                raise RuntimeError("SoundDevice not available")
            if self.running:
                return
            
            self.running = True
            self.clap_count = 0
            self.last_trigger = 0.0
            self.thread = Thread(target = self._run, daemon = True)
            self.thread.start() # not to be confused with the overarching function start()


    def _run(self):
        if not HAS_SOUNDDEVICE:
            return
        try:
            self.stream = sd.InputStream(channels = 1, callback = self._audio_callback)
            with self.stream:
                print("[ClapDetector] Stream opened and listening for claps")
                while self.running:
                    time.sleep(0.1)
        except Exception as e:
            print(f"[ClapDetector] Audio Stream Error: {e}")
        

    def stop(self):
        if not self.running:
            return

        print("[ClapDetector] Stopping detector...")
        self.running = False

        if self.stream:
            try:
                self.stream.close()
                print("[ClapDetector] Stream closed.")
            except Exception as e:
                print(f"[ClapDetector] Error closing stream: {e}")
            self.stream = None

        if self.thread:
            self.thread.join(timeout=1.0)
            print("[ClapDetector] Thread joined.")
            self.thread = None

        print("[ClapDetector] Detector fully stopped.")