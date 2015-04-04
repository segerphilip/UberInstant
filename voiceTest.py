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
    print type(response_text)
    return json.loads(response_text)


def get_lat_long(place_name):
    """
    Given a place name or address, return a (latitude, longitude) tuple
    with the coordinates of the given place.
    """
    url = "https://maps.googleapis.com/maps/api/geocode/json?address=%s" %(place_name.replace(" ","%20"))
    api_res = get_json(url)
    return (api_res['results'][0]['geometry']['location']['lat'],api_res['results'][0]['geometry']['location']['lng'])

def record():
    """ Records wav audio file for later speech recognition processing """

    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    CHUNK = 1024
    RECORD_SECONDS = 5
    WAVE_OUTPUT_FILENAME = "file.wav"
    audio = pyaudio.PyAudio()
    # start Recording
    stream = audio.open(format=FORMAT, channels=CHANNELS,
    rate=RATE, input=True,
    frames_per_buffer=CHUNK)
    print "recording..."


    frames = []
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print "Finished Recording"

    # stop Recording
    stream.stop_stream()
    stream.close()
    audio.terminate()
    waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()


if __name__ == '__main__':
    record()
    r = sr.Recognizer()
    with sr.WavFile("file.wav") as source:              # use "test.wav" as the audio source
        audio = r.record(source)                        # extract audio data from the file

    try:
        output = r.recognize(audio)
        (lat, lon) = get_lat_long(output)
        print("You said: " + output)         # recognize speech using Google Speech Recognition

        print("The latitude and longitude of " + output + " are:")
        print(str(lat) + "  " + str(lon))

    except KeyError:                                    # the API key didn't work
        print("Invalid API key or quota maxed out")
    except LookupError:                                 # speech is unintelligible
        print("Could not understand audio")
