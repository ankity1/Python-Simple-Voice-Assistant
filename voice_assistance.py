"""Automated Calls"""
import os
import playsound
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import speech_recognition as speech
from gtts import gTTS
import time

num = 1


def assistant_speaks(output):
    global num

    # num to rename every audio file
    # with different name to remove ambiguity
    num += 1
    print("Voice Assistant : ", output)

    toSpeak = gTTS(text=output, lang='en', slow=False)
    # saving the audio file given by google text to speech
    file = str(num) + ".mp3"
    toSpeak.save(file)

    # playsound package is used to play the same file.
    playsound.playsound(file, True)
    os.remove(file)

def auto_google():
    """
    Google Data
    :return:
    """
    rObject = speech.Recognizer()
    with speech.Microphone() as source:
        print("Speak...")

        # recording the audio using speech recognition
        audio = rObject.listen(source, phrase_time_limit=5)
    print("Stop.")  # limit 5 secs
    try:
        text = rObject.recognize_google(audio, language='en-US')
        # Chrome exit issue
        chrome_options = Options()
        chrome_options.add_argument("start-maximized")
        chrome_options.add_experimental_option("detach", True)
        # Chrome exit issue
        chrome = webdriver.Chrome('chromedriver.exe', options=chrome_options)
        assistant_speaks('Opening '+ text)
        time.sleep(5)
        chrome.get('https://www.' + text.lower() + '.com/')
        return text

    except:
        assistant_speaks("Could not understand your audio, PLease try again !")
        return 0


if __name__ == "__main__":
    assistant_speaks("Which website you want to work on ?")
    name = auto_google()
