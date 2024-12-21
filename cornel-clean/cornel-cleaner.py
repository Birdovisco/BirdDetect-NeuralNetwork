import os
import csv
import shutil
from pydub import AudioSegment

cur_path = os.path.dirname(__file__)
audio_path = cur_path + "\\cornel-lab\\recordings\\Simon"
database_file = cur_path + "\\cornel-lab\\metadata\\polish_audio.csv"
cleaned_dir = cur_path + "\\cornel-lab-cleaned\\"

# max and min audio duration in milliseconds


max_audio_length = 20_000
min_audio_length = 5_000

# deleted first part of audio
audio_deletion_threshold = 10_000

data = {}

# read database file
with open(database_file, 'r', newline='', encoding='utf-8') as csvfile:
    csvreader = csv.reader(csvfile)
    next(csvreader)
    for row in csvreader:
        data[row[0]] = row[2]

# remove duplicates
species = list(set(data.values()))

# create directory for output database
if not os.path.exists(cleaned_dir):
    os.makedirs(cleaned_dir)

# create directory for each species
for specie in species:
    species_dir = os.path.join(cleaned_dir, specie)
    if os.path.exists(species_dir):
        shutil.rmtree(species_dir)
    os.makedirs(species_dir)

# open recording directory
for filename in os.listdir(audio_path):
    if os.path.isfile(os.path.join(audio_path, filename)):
        recording_id = os.path.splitext(os.path.basename(filename))[0]
        species_dir = cleaned_dir + data[recording_id]

        audio = AudioSegment.from_file(os.path.join(audio_path, filename))
        cleaned_audio = audio[audio_deletion_threshold:]

        # Split the audio into chunks of max_audio_length milliseconds
        for i in range(0, len(cleaned_audio), max_audio_length):
            chunk = cleaned_audio[i:i + max_audio_length]
            if len(chunk) >= min_audio_length:
                chunk_filename = f"{recording_id}_{i // max_audio_length}.wav"
                chunk_path = os.path.join(species_dir, chunk_filename)
                print(f"Exporting {chunk_filename} to {chunk_path}")
                chunk.export(chunk_path, format="wav")
