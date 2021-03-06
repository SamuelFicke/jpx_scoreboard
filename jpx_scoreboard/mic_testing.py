#!/usr/bin/env python3

# NOTE: this example requires PyAudio because it uses the Microphone class

import speech_recognition as sr

# obtain audio from the microphone
r = sr.Recognizer()
with sr.Microphone() as source:
    print("Say something!")
    r.adjust_for_ambient_noise(source)
    audio = r.listen(source)

# recognize speech using Google Speech Recognition
#try:
#    # for testing purposes, we're just using the default API key
#    # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
#    # instead of `r.recognize_google(audio)`
#    print("Google Speech Recognition thinks you said " + r.recognize_google(audio))
#except sr.UnknownValueError:
#    print("Google Speech Recognition could not understand audio")
#except sr.RequestError as e:
#    print("Could not request results from Google Speech Recognition service; {0}".format(e))


# recognize speech using Wit.ai
WIT_AI_KEY = "6OBZBOGKTUZK7TAUIPDWNPZ2S67HAOAT"  # Wit.ai keys are 32-character uppercase alphanumeric strings
try:
    print(r.recognize_wit(audio, key=WIT_AI_KEY))
except sr.UnknownValueError:
    print("Wit.ai could not understand audio")
except sr.RequestError as e:
    print("Could not request results from Wit.ai service; {0}".format(e))

