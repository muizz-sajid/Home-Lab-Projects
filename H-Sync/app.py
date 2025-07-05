from flask import Flask, render_template, request, redirect, url_for, jsonify, flash, Response, stream_with_context
from core.device_manager import DeviceManager
from audio.clap_listener import ClapDetector
from plugins.chromecast.chromecast_driver import ChromecastDevice
import queue
import json
from pathlib import Path

STATIONS_PATH = Path(__file__).parent / "static" / "radio_stations.json"

def load_stations():
    with open(STATIONS_PATH, "r") as f:
        return json.load(f)

RADIO_STATIONS = load_stations()

clap_events = queue.Queue()
clap_detectors = {}

def create_app(config=None):
    app = Flask(__name__)
    cfg = config or {}
    app.config.from_mapping(
        SECRET_KEY=cfg.get('SECRET_KEY', 'dev'),
    )

    manager = DeviceManager()
    manager.load()

    @app.route("/")
    def index():
        global clap_detectors
    
        for detector in clap_detectors.values():
            if detector.running:
                detector.stop()
        
        clap_detectors.clear()

        raw_casts = ChromecastDevice.discover()
        manager.devices = {cast.name: cast for cast in raw_casts}

        devices = manager.list_devices()
        return render_template("index.html", devices = devices)

    @app.route("/device/<name>", methods=["GET", "POST"])
    def device_page(name):
        global clap_detectors

        device = manager.get_device(name)

        if name in clap_detectors:
            old_detector = clap_detectors[name]
            if old_detector.running:
                old_detector.stop()
            del clap_detectors[name]

        if "speaker" in name.lower():
            status = device.get_status()
            return render_template("speakers.html", name=name, status=status, stations=RADIO_STATIONS)
        
        else:

            def clap_trigger():
                app.logger.info(f"[Clap] Detected -> turning on {device.name}")
                clap_events.put(device.name) 
                try:
                    device.turn_on()
                except Exception as e:
                    app.logger.error(f"[Clap] Error turning on device {device.name}: {e}")

            new_detector = ClapDetector(clap_trigger)
            new_detector.start()
            clap_detectors[name] = new_detector
            
            status = device.get_status()
 
            return render_template("device.html", name = name, status = status)

    @app.route("/api/device/<name>/action", methods = ["POST"])
    def device_action(name):
        device = manager.get_device(name)
        if not device:
            return jsonify({"error": "Device not found"}), 404

        data = request.get_json() or {}
        action = data.get("action")

        try:
            if action in ("turn_on", "turn_off", "toggle", "mute", "unmute",
                        "launch_youtube", "launch_netflix", "launch_spotify"):
                getattr(device, action)()
            elif action == "play_media":
                url = data.get("url")
                if not url:
                    return jsonify({"error": "Missing URL"}), 400
                device.play_media(url)

            elif action == "play_youtube":
                query = data.get("query")
                if not query:
                    return jsonify({"error": "Missing search term or URL"}), 400
                device.play_youtube(query)

            elif action == "set_volume":
                lvl = data.get("level")
                if lvl is None:
                    return jsonify({"error": "Missing Level"}), 400
                device.volume(lvl)

            elif action == "volume_up":
                device.volume_up()
            elif action == "volume_down":
                device.volume_down()

            elif action == "playback":
                cmd = data.get("cmd")
                if not cmd:
                    return jsonify({"error": "Missing Command"}), 400
                device.playback(cmd)

            else:
                return jsonify({"error": f"Unknown Action {action}"}), 400

            status = device.get_status()
            return jsonify({"status": status})

        except Exception as e:
            app.logger.error(f"Error running action {action}: {e}", exc_info = True)
            return jsonify({"error": str(e)}), 500  

    @app.route("/device/<name>/events")
    def events(name):
        def event_stream(device_name):
            yield "retry: 1000\n\n"
            yield ": connected\n\n"
            while True:
                try:
                    n = clap_events.get(timeout=5) 
                    yield f"data: {n}\n\n" 
                except queue.Empty:
                    yield ": ping\n\n"  

        return Response(stream_with_context(event_stream(name)), content_type="text/event-stream")

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host = "0.0.0.0", port = 5000, debug = True)
