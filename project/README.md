# Subtitle File Generator
#### Video Demo:  https://youtu.be/0iPa9YVzB0U
#### Description:
This subtitle file generator extracts audio from a video file, processes the audio by splitting it into segments based on silence, detects and identifies the spoken language, and generates subtitles in .srt format. The code automates subtitle generation for any video in any language.

#### Working of project.py:
#### Main Function: main()
This main() function serves as the entry point for the program. It takes the user's input for the video file path and validates the file path and file type to confirm if it is a video that exists at the correct address. If its not then the user is prompted again until a valid address is given. Calls subsequent functions(each of which are explained below) to process the video and then finally, generates and outputs the subtitle file name.



#### Function: extract_audio()
This function loads a video file with the aid of "moviepy" library. It then extracts the audio track from the video and saves it as a separate WAV audio file. The function returns the string "audio.wav", so the subsequent calling function knows where to find the extracted audio. This function is essential for converting a video’s audio into a format suitable for speech-to-text transcription. Keep in mind that the entire video is loaded into RAM, so for large files, this may consume significant memory.

##### <ins>Why Use WAV Format:</ins>
+ Its Uncompressed meaning it keeps the original audio quality.
+ WAV is widely supported by audio processing libraries (like pydub, speech_recognition).
+ Better for Speech Recognition: Lossless quality ensures better transcription accuracy.



#### Function: detect_language(text)
This function determines the language of the provided segment of text using the "langdetect" library. langdetect is based on Google's language detection algorithms which analyzes letter patterns, word frequency, and grammar. In the events that the language is not detected, the function returns "unknown" as a failsafe to prevent the program from crashing. This could happen if there is no text present to analyze or if the language is not supported by the "langdetect" library.



#### Function: split_audio_on_silence(audio_path)
This function loads the audio file, which is in WAV format, using "AudioSegment" from pydub library. It is then divided into smaller segments based on silence as an indicator for division. If a chunk is longer than 15 seconds, it’s split further into 10-second segments to improve transcription accuracy but retains 400 ms of silence at the beginning and end of each split chunk to avoid accidentally cutting off words. All the segments are then finally returned in the form of a list for further processing in the "transcribe_audio_segment" function. This method ensures that the audio is broken into manageable, speech-centric chunks that align well with natural pauses in speech.

##### <ins>Requirements for a silence to be considered a break:</ins>
+ A silence must last at least 500 ms to be considered a break.
+ Silence is considered at -35 dBFS.



#### Function: transcribe_audio_segments(audio_segments)
Since "split_audio_on_silence" function already divided the audio into speech-focused chunks, each chunk is now processed separately. This function, "transcribe_audio_segments(audio_segments)", is designed to automate transcription of segmented speech and it does so by first exporting the audio segments and saving them in temporary WAV files named "temp_chunk.wav" in a specified format (one at a time). The audio is then converted into speech using Google's API but before that, each segment is adjusted to cater and filter out the background noise so that transcription is as accurate as possible. Incase the speech is still unclear to the API, the function adds [Unrecognized Speech] as the subtitle. The function then returns a list of tuples (start_time, end_time, transcribed_text, detected_language), the latter of whom is identified by calling detect_language().

##### <ins>Why Google's API is used:</ins>
+ Google's API supports multiple languages and provides decent accuracy.
+ It can handle different accents, background noise, and various speaking styles.

##### <ins>Why create "temp_chunk.wav" as a temporary file:</ins>
+ speech_recognition requires an actual file or AudioFile object to process audio.
+ WAV format is preferred since it's uncompressed and retains audio quality for better recognition accuracy.

##### <ins>Why delete the temporary file:</ins>
+ Each segment was saved as "temp_chunk.wav", but we no longer need it after the segment is processed.
+ If not removed, multiple temporary files could clutter storage causing storage buildup.



#### Function: save_subtitles(subtitles)

This function automatically generates a subtitle file by iterating over the list of subtitle entries and formatting them (using pysrt) according to the SRT format by ensuring that each subtitle entry has a proper index, timestamp, and text, including language information. The function then saves them to a .srt file which has the name, "subtitles.srt". This formatting makes it compatible with most video players (VLC, YouTube, etc.) and editing softwares. The function also returns "subtitles.srt", allowing other parts of the program to access the generated file.

It was considered to let the user decide what to name the subtitle file but I decided not to pursue it, feeling it moved away from the automated nature of the code in generating a .srt file.



#### Function: clean_up(audio_path)
This function handles the deletion of the temporary audio file, "audio.wav," generated when "extract_audio(video_path)" is called. It ensures that the file is removed only after the subtitles have been successfully created, preventing premature deletion that could result in incomplete subtitles while simultaneously maintaining system organization and ensuring the smooth execution of the program.



#### Usage:
Run the code with python script.py. When prompted, enter the path to a video file (e.g., testvid.mp4).

The code will then generate subtitles.srt.



#### Working of test_project.py
#### Function: test_extract_audio()
This function verifies that the extract_audio function successfully extracts audio from a given video file and saves it correctly.

<ins>Note:</ins> Ensure that testvid.mp4 is available in the working directory before running this test.


#### Function: test_detect_language()
This function confirms that the detect_language function accurately identifies the language of a given text input.


#### Function: test_clean_up()
This function ensures that the clean_up function effectively deletes specified files and handles cases where the file does not exist.


#### Notes
+ All necessary pip installable libraries are listed in "requirements.txt".

+ The project comes with a "testvid.mp4" to use as sample for running the program.

+ Updated FFmpeg is required for pydub and moviepy to handle audio processing.

+ Multi-language support is available but depends on Google Speech Recognition accuracy.

+ Silence detection tuning may be necessary for different audio conditions.

+ Large files may take longer to process due to multiple function calls.
