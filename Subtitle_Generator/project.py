import os
import pysrt

import speech_recognition
sr = speech_recognition

from moviepy import VideoFileClip
from pydub import AudioSegment, silence
from langdetect import detect



def main():
    while True:
        video_path = input("Enter video name: ")

        if not video_path.endswith(".mp4"):
            print("File is not a video. Please try again")
            continue

        if not os.path.exists(video_path):
            print("File not found. Please try again.")
            continue
        else:
            break

    audio_path = extract_audio(video_path)
    audio_segments = split_audio_on_silence(audio_path)
    subtitle_data = transcribe_audio_segments(audio_segments)
    file_name = save_subtitles(subtitle_data)

    print(f"Subtitles saved to {file_name}")

    clean_up(audio_path)



def extract_audio(video_path):
    video = VideoFileClip(video_path)
    video.audio.write_audiofile("audio.wav")
    return "audio.wav"



def split_audio_on_silence(audio_path):
    audio = AudioSegment.from_wav(audio_path)

    chunks = silence.split_on_silence(
        audio,
        min_silence_len=500,
        silence_thresh=-35,
        keep_silence=400
    )

    audio_segments = []
    current_start = 0

    for chunk in chunks:
        duration = len(chunk)
        current_end = current_start + duration

        if duration > 15000:
            count = duration // 10000
            for i in range(count + 1):
                seg_start = current_start + (i * 10000)
                seg_end = min(seg_start + 10000, current_end)
                audio_segments.append((seg_start, seg_end, chunk[i * 10000 : seg_end - current_start]))
        else:
            audio_segments.append((current_start, current_end, chunk))

        current_start = current_end

    return audio_segments



def transcribe_audio_segments(audio_segments):
    recognizer = sr.Recognizer()
    subtitles = []

    for (start, end, chunk) in audio_segments:
        chunk.export("temp_chunk.wav", format="wav")

        with sr.AudioFile("temp_chunk.wav") as file:
            recognizer.adjust_for_ambient_noise(file)
            audio_data = recognizer.record(file)
            try:
                text = recognizer.recognize_google(audio_data)
                language = detect_language(text)
                subtitles.append((start / 1000, end / 1000, text, language))
            except sr.UnknownValueError:
                subtitles.append((start / 1000, end / 1000, "[Unrecognized Speech]", "unknown"))

        os.remove("temp_chunk.wav")

    return subtitles



def detect_language(text):
    try:
        return detect(text)
    except:
        return "unknown"
    


def save_subtitles(subtitles):
    subs = pysrt.SubRipFile()

    for i, (start, end, text, language) in enumerate(subtitles, 1):
        subs.append(pysrt.SubRipItem(
            index=i,
            start=pysrt.SubRipTime(seconds=int(start)),
            end=pysrt.SubRipTime(seconds=int(end)),
            text=f"[{language}] {text}"
        ))

    file_name = "subtitles.srt"
    subs.save(file_name)
    return file_name



def clean_up(audio_path):
    if os.path.exists(audio_path):
        os.remove(audio_path)



if __name__ == "__main__":
    main()
