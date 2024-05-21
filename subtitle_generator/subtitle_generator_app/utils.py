import os
import sys
import moviepy.editor as mp
from IPython.display import Video, Audio, display
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
from datetime import timedelta # for working with time intervals
from googletrans import Translator

# import subprocess
import whisper # for transcription



def extract_audio(video):
    """
    This function gets a path to video file as input,
    extracts the audio from video and returns the audio file path
    """
    # Extract the audio from the video
    audio = video.audio
    # Get the directory path of the video file
    # dir = os.path.dirname(video_path)
    # Define the path for the extracted audio file
    # audio_path = os.path.splitext(video_path)[0] + '.mp3'
    audio_path = os.path.splitext(video.filename)[0] + '.mp3'
    # Save the extracted audio to a file
    audio.write_audiofile(audio_path)
    return audio_path

def transcribe_audio(audio_path):
    """
    This function gets the path to the audio
    and uses Whisper library to extract transcription from the audio
    """

    model = whisper.load_model("medium")  # Change this to your desired model
    print("Whisper model loaded.")
    options = dict(beam_size=5, best_of=5)
    translate_options = dict(task="translate", **options)
    transcribe = model.transcribe(audio=audio_path, **translate_options)
    if transcribe is None or 'segments' not in transcribe:
        print("Transcription failed.")
        return []
    segments = transcribe['segments']
    return segments


def translate_text(text, selected_language):
    """
    This function translates text to the desired language
    """
    try:
        translator = Translator()
        translated_text = translator.translate(text, dest=selected_language)
        return translated_text.text
    except Exception as e:
        # Log the error for debugging purposes
        return "Translation failed"


def create_subtitle_clips(transcription, select_language ,videosize ,fontsize=30, font='Arial', color='white', bg_color = 'black', debug = False):
    """
    This function extracts text, start time, and end time
    from transcription and generates subtitle clips
    """
    subtitle_clips = []
    

    for idx, entry in enumerate(transcription):
        start_time = entry['start']
        end_time = entry['end']
        text = translate_text(entry['text'][1:], select_language)
        duration = end_time - start_time
        video_width, video_height = videosize
        text_clip = TextClip(text, fontsize=30, font='Arial', color='white',bg_color = 'black',
                             size=(video_width*3/4, None), method='caption').set_start(start_time).set_duration(duration)

        subtitle_x_position = ('bottom')

        subtitle_y_position = video_height* 4 / 5

        text_position = (subtitle_x_position, subtitle_y_position)

        subtitle_clips.append(text_clip.set_position(text_position))

    return subtitle_clips