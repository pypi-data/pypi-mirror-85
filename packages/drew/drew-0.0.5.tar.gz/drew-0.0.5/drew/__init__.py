import os, time, winsound

def drew():
    os.system('cls')
    directory = os.path.dirname(os.path.abspath(__file__))
    frameDirectory = os.path.join(directory, "Frames")
    #frameDirectory = directory
    frames = []
    cycles = 3
    audioDirectory = os.path.join(directory, "Audio")
    #audioDirectory = directory
    soundFile = os.path.join(audioDirectory, "stayinAlive.wav")

    for filename in os.listdir(frameDirectory):
        with open(os.path.join(frameDirectory, filename), 'r', encoding='utf8') as f:
            frames.append(f.readlines())

    winsound.PlaySound(soundFile, winsound.SND_FILENAME|winsound.SND_ASYNC)
    for cycle in range(cycles):
        for frame in frames:
            print("".join(frame))
            time.sleep(.55)
            os.system('cls')