import json, os
import pyttsx3, vosk, pyaudio, requests
import users
import random


class Users(object):
    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender


tts = pyttsx3.init()
voices = tts.getProperty('voices')
tts.setProperty('voices', 'en')


for voice in voices:
    if voice.name == 'Microsoft David Desktop - English (United States)':
        tts.setProperty('voice', voice.id)


model = vosk.Model('C:/Users/serjk/PycharmProjects/vosk-model-small-ru-0.4')
record = vosk.KaldiRecognizer(model, 16000)
pa = pyaudio.PyAudio()
stream = pa.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
stream.start_stream()


def listen():
    while True:
        data = stream.read(4000, exception_on_overflow=False)
        if record.AcceptWaveform(data) and len(data) > 0:
            answer = json.loads(record.Result())
            if answer['text']:
                yield answer['text']


def speak(say):
    tts.say(say)
    tts.runAndWait()


names = ['Петя', 'Вася', 'Лена', 'Серёжа', 'Ира', 'Егор', 'Маша']
genders = ['male', 'female']
arr = []


def create():
    print('КОМАНДА: создать')
    user = Users(random.choice(names), round(random.uniform(0, 100)), random.choice(genders))
    arr.append(user)
    speak('пользователь создан')


def create_3():
    print('КОМАНДА: создать три')
    user1 = Users(random.choice(names), round(random.uniform(0, 100)), random.choice(genders))
    user2 = Users(random.choice(names), round(random.uniform(0, 100)), random.choice(genders))
    user3 = Users(random.choice(names), round(random.uniform(0, 100)), random.choice(genders))
    arr.extend([user1, user2, user3])
    speak('было создано три пользователя')


def user_list():
    print('КОМАНДА: список')
    speak('вот список пользователей')
    i = 1
    for user in arr:
        print('     User_' + str(i) + ': {' + str(user.name) + ', ' + str(user.age) + ', ' + str(user.gender) + '}')
        i+=1

def delete():
    print('КОМАНДА: удалить')
    arr.pop(0)
    speak('первый пользователь удален')


def clear():
    print('КОМАНДА: очистить')
    arr.clear()
    speak('список очищен')


print('Слушаю внимательно!')
speak('Слушаю внимательно!')
for text in listen():
    if text == 'создать':
        create()
    if text == 'создать три':
        create_3()
    elif text == 'список':
        user_list()
    elif text == 'удалить':
        delete()
    elif text == 'очистить':
        clear()
    elif text == 'сохранить':
        print('КОМАНДА: сохранить')
        with open('result.txt', 'w') as f:
            answer = ''
            i = 1
            for user in arr:
                answer += '     User_' + str(i) + ': {' + str(user.name) + ', ' + str(user.age) + ', ' + str(user.gender) + '}'
                i += 1
            f.write(answer)
            speak('список записан в файл')
    else:
        pass
