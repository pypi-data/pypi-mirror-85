
import speech as speechsdk
from ngchat_speech import audio as audio
from ngchat_speech.utils import Wave
from datetime import datetime
# import librosa
USE_STREAM_METHOD = True
SAVE_FINAL_AUDIO_DATA_TO_FILE = False

if __name__ == "__main__":
    speech_config = speechsdk.SpeechConfig(
        account_id="speechdemo",
        password="12345678",
        speech_synthesis_language="zh-tw",
        speech_synthesis_voice_name="lintong",
        speech_synthesis_output_format_id="riff-22khz-16bit-mono-pcm",
        speech_synthesis_output_pitch=0.0,
        speech_synthesis_output_speed=1.0
    )
    if USE_STREAM_METHOD is False:
        audio_config = audio.AudioOutputConfig(filename="output.wav")
    else:
        audio_stream = audio.AudioOutputStream()
        audio_config = audio.AudioOutputConfig(stream=audio_stream)
    speech_synthesizer = speechsdk.SpeechSynthesizer(
        speech_config=speech_config,
        audio_config=audio_config
    )

    timestr = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    audio_filename = f"audiosaved_{timestr}.wav"
    audiofile = Wave(audio_filename, 'wb')
    audiofile.setnchannels(1)
    audiofile.setsampwidth(2)
    audiofile.setframerate(22050)

    def save_raw_data(audio_data):
        print("saving raw data")
        audiofile.writeframes(audio_data)

    speech_synthesizer.synthesis_started.connect(lambda : print("synthesis started"))
    speech_synthesizer.synthesis_canceled.connect(lambda : print("synthesis canceled"))
    if USE_STREAM_METHOD is False:
        speech_synthesizer.synthesizing.connect(lambda audio_data: print("synthesizing"))
        speech_synthesizer.synthesis_completed.connect(lambda audio_data: print("synthesis completed"))
    else:
        speech_synthesizer.synthesizing.connect(save_raw_data)
        speech_synthesizer.synthesis_completed.connect(save_raw_data)

    result = speech_synthesizer.speak_text("爲什麽模範生容易被綁架，因爲他一副好榜樣。")
    # result = speech_synthesizer.speak_text_async("爲什麽模範生容易被綁架，因爲他一副好榜樣。").get()
    # result = speech_synthesizer.speak_ssml_async("Python是一種廣泛使用的解釋型，高級編程，通用型編程語言。 Python支持多種編程範式，包括面向對象，結構化，指令式，函數式和反射式編程。它擁有動態類型系統和垃圾回收功能，能夠自動管理內存使用，並且其本身擁有一個巨大而廣泛的標準庫。").get()

    audiofile.close()

    if result.reason == speechsdk.ResultReason.ResultReason_SynthesizingAudioCompleted:
        print("finished speech synthesizing")

        if SAVE_FINAL_AUDIO_DATA_TO_FILE is True:
            audio_data = audio_stream.read()
            timestr = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
            audio_filename = f"output_{timestr}.wav"
            audio = Wave("output.wav", 'wb')
            audio.setnchannels(1)
            audio.setsampwidth(2)
            audio.setframerate(22050)
            audio.writeframes(audio_data)
            audio.close()

        # resample 22050 to 16000 if needed
        # y, sr = librosa.load('output.wav', sr=16000)
        # librosa.output.write_wav("resampled.wav", y, sr)
