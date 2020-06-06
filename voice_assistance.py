"""Automated Calls"""
import os
import playsound
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import speech_recognition as speech
from gtts import gTTS
import time
import requests
import cv2
import logging


num = 1
api_key = 'XXXXXXXXXXXXXXXXXXXXX'


def assistant_speaks(output):
    """
    Assistant Google
    :param output:
    :return:
    """
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
    audio = ''

    with speech.Microphone() as source:
        print("Speak...")

        # recording the audio using speech recognition
        audio = rObject.listen(source, phrase_time_limit=5)
    print("Stop.")  # limit 5 secs
    flag = 0
    while 1:
        try:
            if flag == 0:
                text = rObject.recognize_google(audio, language='en-US')
                response = get_keyword(text)
                if response == 'stop':
                    assistant_speaks("Bye Ankit, hope you enjoy talking with me!!")
                    return
                if response:
                    assistant_speaks(response)
                flag += 1
            else:
                assistant_speaks("Hey Ankit, Anything else you want help with?")
                auto_google()
        except Exception as e:
            logging.error(e)
            assistant_speaks("Could not understand your audio, Please try again !")
            auto_google()


def get_keyword(text):
    """
    Search Particular Keyword
    :param text:
    :return:
    """
    if 'weather' in text.lower():
        return get_weather()
    elif 'date' in text.lower():
        return get_date()
    elif 'time' in text.lower():
        return get_time()
    elif 'stop' in text.lower() or 'bye' in text.lower():
        return 'stop'
    elif 'camera' in text.lower():
        return open_camera()
    else:
        if text:
            words = text.split(' ')
            words = [word.lower() for word in words]
            value = words[words.index('open') + 1] if 'open' in words else ''
            if value:
                return get_web_page(value)
            return 'stop'
        return 'stop'


def get_weather():
    """
    Get Current Weather Report
    :return:
    """
    r = requests.get('http://api.openweathermap.org/data/2.5/weather?q=Ghaziabad&appid=%s' % api_key)
    if r.status_code == 200:
        weather = eval(r.content.decode("UTF-8"))['weather'][0]['description']
        humidity = eval(r.content.decode("UTF-8"))['main']['humidity']
        temp = eval(r.content.decode("UTF-8"))['main']['temp'] - 273.15
        temp = '%.2f' % temp
        return "It's " + weather + " with humidity over " + str(humidity) + " and temperature over "+ str(temp) + " degree celsius"
    return 'Unable to fetch weather report'


def get_date():
    """
    Get Date
    :return:
    """
    date = time.strftime('%d %B')
    return "Today's Date is " + str(date)


def get_time():
    """
    Get Time
    :return:
    """
    current_time = time.strftime("%I:%M %p")
    return "Now Time is " + str(current_time)


def open_camera():
    """
    open camera
    :return:
    """
    # define a video capture object
    vid = cv2.VideoCapture(0)
    while True:
        # Capture the video frame
        # by frame
        ret, frame = vid.read()
        # Display the resulting frame
        cv2.imshow('frame', frame)
        # the 'q' button is set as the
        # quitting button you may use any
        # desired button of your choice
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    # After the loop release the cap object
    vid.release()
    # Destroy all the windows
    cv2.destroyAllWindows()
    return None


def get_web_page(text):
    """
    Open Web page
    :param text:
    :return:
    """
    # Chrome exit issue
    chrome_options = Options()
    chrome_options.add_argument("start-maximized")
    chrome_options.add_experimental_option("detach", True)
    # Chrome exit issue
    chrome = webdriver.Chrome('chromedriver.exe', options=chrome_options)
    assistant_speaks('Opening '+ text)
    time.sleep(5)
    chrome.get('https://www.' + text.lower() + '.com/')
    return None


if __name__ == "__main__":
    assistant_speaks("Hey Ankit, how may I help you?")
    auto_google()
