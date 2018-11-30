
import pyaudio
import wave
from array import array

FORMAT=pyaudio.paInt16
CHANNELS=2
RATE=44100
CHUNK=1024
RECORD_SECONDS=5
FILE_NAME="RECORDING.wav"

def listen():

    audio=pyaudio.PyAudio() #instantiate the pyaudio

    #recording prerequisites
    stream=audio.open(format=FORMAT,channels=CHANNELS, 
                      rate=RATE,
                      input=True,
                      frames_per_buffer=CHUNK)

    #starting recording
    frames=[]


#     for i in range(0,int(RATE/CHUNK*RECORD_SECONDS)):
        # data=stream.read(CHUNK)
        # data_chunk=array('h',data)
        # vol=max(data_chunk)
        # if(vol>=500):
            # frames.append(data)


# This piece attemps to not limit recording to n seconds
# but to make it variable depending on what is being said
            
    recording_left = 88 # 44 is roughly a second
    chunk_n = 0
    while recording_left:
        chunk_n += 1
        # print("working on chunk: {}".format(chunk_n))
        data=stream.read(CHUNK)
        data_chunk=array('h',data)
        vol=max(data_chunk)
        if(vol>=1000):
            frames.append(data)
            recording_left = 44 # If there is volume, we have 1 more second to record
        else:
            recording_left -= 1

        # print("volume: {}".format(vol))
        # print("recording_left: {}".format(recording_left))

        if chunk_n > 1000:
            recording_left = 0

    #end of recording
    stream.stop_stream()
    stream.close()
    audio.terminate()
    #writing to file
    wavfile=wave.open(FILE_NAME,'wb')
    wavfile.setnchannels(CHANNELS)
    wavfile.setsampwidth(audio.get_sample_size(FORMAT))
    wavfile.setframerate(RATE)
    wavfile.writeframes(b''.join(frames))#append frames recorded to file
    wavfile.close()

