import os
import time
import speech_recognition as sr
from fuzzywuzzy import fuzz
import pyttsx3
import datetime
import webbrowser


opts = {
    "alias": ('джарвис', 'дарвис', 'джарвиз', 'джервиз', 'джервис', 'дарвис',
              'дарвиз', 'джорвиз', 'джорвис', 'дарвис', 'дорвис', 'jarvis'),
    "tbr": ('скажи', 'расскажи', 'покажи', 'сколько', 'произнеси', 'открой'),
    "cmds": {
        "ctime": ('текущее время', 'сейчас времени', 'который час'),
        "browser": ('открой браузер', 'открой гугл')
    }
}


def speak(what):
    print(what)
    speak_engine.say(what)
    speak_engine.runAndWait()
    speak_engine.stop()


def callback(recognizer, audio):
    try:
        voice = recognizer.recognize_google(audio, language="ru-RU").lower()
        print("[log] Распознано: " + voice)

        if voice.startswith(opts["alias"]):

            cmd = voice

            for x in opts['alias']:
                cmd = cmd.replace(x, "").strip()

            for x in opts['tbr']:
                cmd = cmd.replace(x, "").strip()

            cmd = recognize_cmd(cmd)
            execute_cmd(cmd['cmd'])

    except sr.UnknownValueError:
        print("[log] Голос не распознан!")
    except sr.RequestError as e:
        print("[log] Неизвестная ошибка, проверьте интернет!")


def recognize_cmd(cmd):
    RC = {'cmd': '', 'percent': 0}
    for c, v in opts['cmds'].items():

        for x in v:
            vrt = fuzz.ratio(cmd, x)
            if vrt > RC['percent']:
                RC['cmd'] = c
                RC['percent'] = vrt

    return RC


def execute_cmd(cmd):
    if cmd == 'browser':
        webbrowser.open('https://www.google.com/')
        speak('Браузер открыт, сэр. ')

    elif cmd == 'ctime':
        now = datetime.datetime.now()
        speak("Сейчас " + str(now.hour) + ' Часов' +
              ":" + str(now.minute) + ' Минут.')
    else:
        print('Команда не распознана, повторите!')


r = sr.Recognizer()
m = sr.Microphone(device_index=1)

with m as source:
    r.adjust_for_ambient_noise(source)

speak_engine = pyttsx3.init()


voices = speak_engine.getProperty('voices')
speak_engine.setProperty('voice', voices[0].id)


speak("Здравствуйте Никита, Джарвис вас слушает")

stop_listening = r.listen_in_background(m, callback)
while True:
    time.sleep(0.1)  # infinity loop
