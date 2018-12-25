
from gtts import gTTS
import speech_recognition as sr

import json
import os

from ai_assistant import AI_Assistant
from record import listen


def get_content():
    print("listening...")
    listen() # This would create new wave file
    r = sr.Recognizer()
    my_recording = sr.AudioFile("RECORDING.wav")

    with my_recording as source: 
        audio = r.record(source) 
    
    return r.recognize_google(audio)


if __name__ == "__main__":

    ai_assistant = AI_Assistant()

    while True:

        try:
            content = get_content().lower()
            print("\033[0;32m" + "received content: {}".format(content) + "\033[0m")

            if any(x in content for x in ("alexa")):

                if "play" in content:
                    ai_assistant.play_music(content)

                elif all(x in content for x in ("is", "prime")) and any(x.isdigit() for x in content):
                    ai_assistant.is_prime(content)

                elif any(x in content for x in ("plus", "minus", "times", "-", "+", "/", "*")):
                    ai_assistant.do_math(content)

                elif all(x in content for x in ("is", "prime")) and any(x.isdigit() for x in content):
                    ai_assistant.is_prime(content)

                elif "tell" in content and "joke" in content:
                    ai_assistant.tell_a_joke()

                elif "fact" in content and "interesting" in content:
                    ai_assistant.tell_an_interesting_fact()

                elif "price" in content and "stock" in content:
                    ai_assistant.get_stock_price(content)

                elif "repeat" in content:
                    ai_assistant.repeat(content)

                ai_assistant.handle_simple_response(content)

        except Exception as exc:
            print("Found no valid content, exception: {}".format(exc))
            import time
            time.sleep(1)

