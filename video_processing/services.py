import os
import shutil
from django.conf import settings
from .generate.youtube_handler import YouTubeHandler
from .generate.transcription import TranscriptionService
from .generate.quiz_generator import QuizGenerator


class VideoProcessingService:
    """Main service that orchestrates the entire video processing pipeline"""

    @staticmethod
    def process_video_and_create_quiz(quiz_id):
        """
        Main fuction to process video and create quiz
        """
        from quizzes.models import Quiz, Question

        quiz = Quiz.objects.get(id=quiz_id)
        audio_file = None
        temp_dir = None

        try:
            """validate URLs"""
            YouTubeHandler.validate_url(quiz.video_url)

            """extract title"""
            video_info = YouTubeHandler.extract_video_info(quiz.video_url)
            quiz.title = video_info['title']
            quiz.save()

            """audio download in temporary directory"""
            audio_file = YouTubeHandler.download_audio(quiz.video_url)
            temp_dir = os.path.dirname(audio_file)  # Merke dir das temp directory

            """transcribe audio to text"""
            transcription_service = TranscriptionService(model_size='base')
            transcript = transcription_service.transcribe_audio(audio_file)
            quiz.transcript = transcript
            quiz.save()

            """generate quiz questions from transcript"""
            quiz_generator = QuizGenerator()
            questions_data = quiz_generator.generate_quiz_from_transcript(
                transcript,
                num_questions=10
            )

            """create question objects from generated data"""
            for idx, q_data in enumerate(questions_data):
                Question.objects.create(
                    quiz=quiz,
                    question_title=q_data['question_title'],
                    option_a=q_data['option_a'],
                    option_b=q_data['option_b'],
                    option_c=q_data['option_c'],
                    option_d=q_data['option_d'],
                    correct_answer=q_data['correct_answer'],
                    order=idx + 1
                )
            quiz.status = 'completed'
            quiz.save()

        except Exception as e:
            """set quiz status to failed on error"""
            quiz.status = 'failed'
            quiz.description = f"Error: {str(e)}"
            quiz.save()
            raise

        finally:
            """cleanup temporary files"""
            if temp_dir and os.path.exists(temp_dir):
                try:
                    shutil.rmtree(temp_dir)
                    print(f"Cleaned up temporary directory: {temp_dir}")
                except Exception as cleanup_error:
                    print(f"Warning: Could not clean up temp directory: {cleanup_error}")