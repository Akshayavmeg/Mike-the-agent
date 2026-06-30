from faster_whisper import WhisperModel
import sounddevice as sd
from scipy.io.wavfile import write

from config import RECORD_DURATION, SAMPLE_RATE, WHISPER_MODEL


class SpeechRecognizer:
    def __init__(self):
        self.model = WhisperModel(WHISPER_MODEL)

    def listen(self):
        """
        Record audio from the microphone.
        Returns the recognized text.
        """

        print("🎤 Speak now...")

        audio = sd.rec(
            int(RECORD_DURATION * SAMPLE_RATE),
            samplerate=SAMPLE_RATE,
            channels=1,
            dtype="int16"
        )

        sd.wait()

        audio_path = "recordings/recording.wav"

        write(audio_path, SAMPLE_RATE, audio)

        print("Transcribing...")

        segments, _ = self.model.transcribe(audio_path)

        command = ""

        for segment in segments:
            command += segment.text

        command = command.strip().lower()

        print(f"Heard: {command}")

        return command
