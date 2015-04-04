import urllib2
import urllib
import json
import re
import speech_recognition as sr
import pyaudio
import wave

def get_json(url):
    """
    Given a properly formatted URL for a JSON web API request, return
    a Python JSON object containing the response to that request.
    """
    f = urllib2.urlopen(url)
    response_text = f.read()
    return json.loads(response_text)


def get_lat_long(place_name):
    """
    Given a place name or address, return a (latitude, longitude) tuple
    with the coordinates of the given place.
    """
    url = "https://maps.googleapis.com/maps/api/geocode/json?address=%s" %(place_name.replace(" ","%20"))
    api_res = get_json(url)
    return (api_res['results'][0]['geometry']['location']['lat'],api_res['results'][0]['geometry']['location']['lng'])


if __name__ == '__main__':
    r = sr.Recognizer()
    with sr.Microphone() as source:                # use the default microphone as the audio source
        audio = r.listen(source)                   # listen for the first phrase and extract it into audio data

    try:
        print("You said " + r.recognize(audio))    # recognize speech using Google Speech Recognition
    except LookupError:                            # speech is unintelligible
        print("Could not understand audio")
