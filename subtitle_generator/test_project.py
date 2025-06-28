import os
from project import extract_audio, detect_language, clean_up


def test_extract_audio():
    video_path = "testvid.mp4"
    audio_path = extract_audio(video_path)
    assert os.path.exists(audio_path)
    os.remove(audio_path)



def test_detect_language():
    assert detect_language("Hello, how are you?") == "en"
    assert detect_language("Bonjour, comment ça va?") == "fr"
    assert detect_language("") == "unknown"



def test_clean_up():
    test_audio_path = "test_audio.wav"

    with open(test_audio_path, "w") as f:
        f.write("This is a test file.")

    assert os.path.exists(test_audio_path)
    clean_up(test_audio_path)
    assert not os.path.exists(test_audio_path)


    test_audio_path = "test_audio.wav"
    if os.path.exists(test_audio_path):
        os.remove(test_audio_path)
    clean_up(test_audio_path)
    assert not os.path.exists(test_audio_path)
