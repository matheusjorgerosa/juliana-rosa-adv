import os
import time
import argparse
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def setup_gemini():
    """Configures the Gemini API with the API key."""
    api_key = AIzaSyCGK7RkxzOTC4sCPN_SNhYqmn7xkwGgIdI
    if not api_key:
        raise ValueError("GOOGLE_API_KEY not found in environment variables. Please set it in .env file.")
    genai.configure(api_key=api_key)

def upload_to_gemini(path, mime_type=None):
    """Uploads the given file to Gemini.

    See https://ai.google.dev/gemini-api/docs/prompting_with_media
    """
    file = genai.upload_file(path, mime_type=mime_type)
    print(f"Uploaded file '{file.display_name}' as: {file.uri}")
    return file

def wait_for_files_active(files):
    """Waits for the given files to be active.

    Some files uploaded to the Gemini API need to be processed before they can
    be used as prompt inputs. The status can be seen by querying the file's
    "state" field.

    This implementation relies on the file's `name` field being equivalent to
    the name of the file that was uploaded.
    """
    print("Waiting for file processing...")
    for name in (file.name for file in files):
        file = genai.get_file(name)
        while file.state.name == "PROCESSING":
            print(".", end="", flush=True)
            time.sleep(10)
            file = genai.get_file(name)
        if file.state.name != "ACTIVE":
            raise Exception(f"File {file.name} failed to process")
    print("...all files ready")
    print()

def transcribe_audio(audio_path, model_name="gemini-2.5-pro"):
    """Transcribes the audio file using Gemini."""
    setup_gemini()

    # Create the model
    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 64,
        "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel(
        model_name=model_name,
        generation_config=generation_config,
    )

    # Upload the audio file
    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"Audio file not found: {audio_path}")

    print(f"Uploading {audio_path}...")
    # Determine mime_type based on extension if needed, but genai usually handles it.
    # For safety, we can let it auto-detect or specify if known.
    # Common audio formats: mp3, wav, aac, flac, ogg

    files = [upload_to_gemini(audio_path)]
    wait_for_files_active(files)

    chat_session = model.start_chat(
        history=[
            {
                "role": "user",
                "parts": [
                    files[0],
                    "Please transcribe this audio file accurately. Identify different speakers. Start a new line every time the speaker changes. Format as 'Speaker [Label]: [Text]'. Output only the transcription text.",
                ],
            },
        ]
    )

    response = chat_session.send_message("Transcribe audio with speaker diarization")
    return response.text

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Transcribe audio using Gemini API")
    parser.add_argument("audio_file", help="Path to the audio file to transcribe")
    parser.add_argument("--model", default="gemini-2.5-pro", help="Gemini model to use (default: gemini-2.5-pro)")
    args = parser.parse_args()

    try:
        transcription = transcribe_audio(args.audio_file, model_name=args.model)
        print("-" * 20)
        print("Transcription:")
        print("-" * 20)
        print(transcription)
    except Exception as e:
        print(f"Error: {e}")
