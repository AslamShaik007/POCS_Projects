from django.shortcuts import render
from rest_framework.views import APIView
from .utils import extract_audio, transcribe_audio, translate_text, create_subtitle_clips
from moviepy.editor import VideoFileClip, CompositeVideoClip, TextClip
import os
import numpy as np
from django.http import JsonResponse, HttpResponse
# Create your views here.



def generate_subtitles(request):
    if request.method == 'POST':
        print("method", request.method)
        print("file", request.FILES)
        print("language",  request.POST.get('language'))
        # Assuming you have a file upload form field named 'video_file'
        video_file = request.FILES.get('file[]')
        selected_language = request.POST.get('language')  # Get selected language

        if video_file:
            root_directory = 'media/'
            if not os.path.exists(root_directory):
                os.makedirs(root_directory)

            video_filename = video_file.name
            video_path = os.path.join(root_directory, video_filename)

            with open(video_path, 'wb+') as destination:
                for chunk in video_file.chunks():
                    destination.write(chunk)

            video_clip = VideoFileClip(video_path)
            transcription = transcribe_audio(video_path)

            translated_subtitles = []
            for entry in transcription:
                text = entry['text'][1:]  # Remove any leading whitespace
                translated_text = translate_text(text, selected_language)
                translated_subtitles.append({
                    'start': entry['start'],
                    'end': entry['end'],
                    'text': translated_text,
                })
            subtitles_data = create_subtitle_clips(translated_subtitles, select_language=selected_language, videosize=(640, 480), fontsize=30, font='Arial', color='white', bg_color = 'black')
            subtitles = []
            for entry in translated_subtitles:
                subtitle_clip = next((clip for clip in subtitles_data if clip.start == entry['start'] and clip.end == entry['end']), None)
                if subtitle_clip:
                    subtitle_dict = {
                        'start': subtitle_clip.start,
                        'end': subtitle_clip.end,
                        'text': entry['text'],
                    }
                    subtitles.append(subtitle_dict)
            output_video = CompositeVideoClip([video_clip] + [TextClip(subtitle['text'], fontsize=30, color='white', bg_color = 'black').set_position(("bottom")).set_start(subtitle['start']).set_end(subtitle['end']) for subtitle in subtitles])
            output_video_filename = os.path.splitext(video_filename)[0] + '_subtitled.mp4'
            output_video_path = os.path.join(root_directory, output_video_filename)
            output_video.write_videofile(output_video_path, codec='libx264', audio_codec='aac')
            return render(request, 'result.html', {"video": output_video_filename})
    else:
        return render(request, 'home.html')














































# def generate_subtitles(request):
#     if request.method == 'POST':
#         video_file = request.FILES.get('video_file')
#         selected_language = request.POST.get('language')

#         if video_file:
#             try:
#                 # Check if 'media/uploads/' directory exists
#                 uploads_directory = 'media/uploads/'
#                 if not os.path.exists(uploads_directory):
#                     os.makedirs(uploads_directory)

#                 # Construct the video path
#                 video_path = os.path.join(uploads_directory, video_file.name)

#                 # Check if the video with the same name already exists and handle it accordingly
#                 if os.path.exists(video_path):
#                     os.remove(video_path)  # Optionally, replace the existing video

#                 # Save the uploaded video to the specified path
#                 with open(video_path, 'wb+') as destination:
#                     for chunk in video_file.chunks():
#                         destination.write(chunk)

#                 # Extract existing subtitles from the video if they exist (you'll need to implement this)
#                 existing_subtitles = extract_existing_subtitles(video_path)

#                 # Open the video file with moviepy to extract audio
#                 video_clip = VideoFileClip(video_path)

#                 # Save the audio as a separate file
#                 audio_path = os.path.splitext(video_path)[0] + '.wav'
#                 video_clip.audio.write_audiofile(audio_path)

#                 # Transcribe the audio directly from the video_clip
#                 transcription = transcribe_audio(audio_path)

#                 # Translate subtitles to the selected language
#                 translated_subtitles = []
#                 for entry in transcription:
#                     text = entry['text'][1:]  # Remove any leading whitespace
#                     translated_text = translate_text(text, selected_language)
#                     translated_subtitles.append({
#                         'start': entry['start'],
#                         'end': entry['end'],
#                         'text': translated_text,
#                     })

#                 # Merge existing and translated subtitles
#                 all_subtitles = merge_subtitles(existing_subtitles, translated_subtitles)

#                 # Create subtitle clips
#                 subtitle_clips = create_subtitle_clips(all_subtitles, select_language=selected_language, videosize=(640, 480), fontsize=24, font='Arial', color='yellow')

#                 # Set the output path for the output subtitled video
#                 output_video_path = os.path.splitext(video_path)[0] + '_subtitled.mp4'

#                 # Add subtitles to the video
#                 output_video = add_subtitles_to_video(video_clip, subtitle_clips)

#                 # Write the video with subtitles to the output path
#                 output_video.write_videofile(output_video_path, codec='libx264', audio_codec='aac')

#                 return JsonResponse({'subtitles': all_subtitles})

#             except Exception as e:
#                 # Handle any exceptions and log them
#                 print(f"Error: {str(e)}")
#                 return JsonResponse({'error': 'An error occurred while processing the video.'})

#     return render(request, 'subtitle.html')