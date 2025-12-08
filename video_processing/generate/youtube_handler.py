import yt_dlp
import re
import tempfile
import os
import shutil
from django.core.exceptions import ValidationError


class YouTubeHandler:
    """Handles YouTube URL validation and audio download"""

    @staticmethod
    def validate_url(url):
        """Validates if the providef URL is a valid Youtube link"""
        youtube_regex = (
            r'(https?://)?(www\.)?'
            r'(youtube|youtu|youtube-nocookie)\.(com|be)/'
            r'(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})'
        )

        youtube_match = re.match(youtube_regex, url)
        if not youtube_match:
            raise ValidationError("Invalid YouTube URL")

        return True

    @staticmethod
    def extract_video_info(url):
        """Extracts vidoe information without downloading"""
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return {
                'title': info.get('title'),
                'duration': info.get('duration'),
                'description': info.get('description'),
            }

    @staticmethod
    def download_audio(url):
        """
        Download audio from a YouTube video to a temporary directory.
        Returns: Path to the downloaded audio file.
        """
        temp_dir = tempfile.mkdtemp(prefix='youtube_audio_')

        """Define output template for audio file"""
        output_template = os.path.join(temp_dir, 'audio')

        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': output_template,
            'quiet': True,
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            """Define full path to the audio file"""
            audio_file = f"{output_template}.mp3"

            if not os.path.exists(audio_file):
                raise FileNotFoundError(f"Audio file was not created at {audio_file}")

            return audio_file

        except Exception as error:
            """When an error occurs, clean up the temp directory"""
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
            raise error