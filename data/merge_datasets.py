import os
import shutil
from collections import defaultdict
from tqdm import tqdm

def create_dir_structure(base_path, sets, bird_classes):
    os.makedirs(base_path, exist_ok=True)
    for set_name in sets:
        for bird in bird_classes:
            os.makedirs(os.path.join(base_path, set_name, bird), exist_ok=True)

def move_files_to_sets(files, destination_dir, set_name):
    for file_path, bird_name in tqdm(files, desc=f"Moving files to {set_name}", unit="file"):
        dest_dir = os.path.join(destination_dir, set_name, bird_name)
        os.makedirs(dest_dir, exist_ok=True)
        shutil.move(file_path, dest_dir)

def split_dataset(files_grouped, proportions):
    split = {"train": [], "val": [], "test": []}
    total_files = sum(len(files) for files in files_grouped.values())
    
    train_limit = int(total_files * proportions[0])
    val_limit = train_limit + int(total_files * proportions[1])

    current_count = 0
    for files in files_grouped.values():
        if current_count < train_limit:
            split["train"].extend(files)
        elif current_count < val_limit:
            split["val"].extend(files)
        else:
            split["test"].extend(files)
        current_count += len(files)

    return split

def merge_datasets(dataset1_dir, dataset2_dir, output_dir):
    sets = ["train", "val", "test"]

    # Collect all files from the first dataset, already split into sets
    dataset1_split = {set_name: [] for set_name in sets}
    bird_classes = set()
    for set_name in sets:
        set_path = os.path.join(dataset1_dir, set_name)
        for bird in os.listdir(set_path):
            bird_path = os.path.join(set_path, bird)
            if os.path.isdir(bird_path):
                bird_classes.add(bird)
                files = [(os.path.join(bird_path, f), bird) for f in os.listdir(bird_path) if f.endswith(".mp3") or f.endswith(".wav")]
                dataset1_split[set_name].extend(files)

    # Collect files from the second dataset (cornel-lab), grouped by original number (to keep chunks from the same recording in the same set)
    dataset2_files_grouped = defaultdict(list)
    for bird in os.listdir(dataset2_dir):
        bird_path = os.path.join(dataset2_dir, bird)
        if os.path.isdir(bird_path):
            bird_classes.add(bird)
            for file in os.listdir(bird_path):
                if file.endswith(".wav") or file.endswith(".mp3"):
                    number = file.split("_")[0]  # Extract the original file number
                    dataset2_files_grouped[(bird, number)].append((os.path.join(bird_path, file), bird))

    dataset2_split = split_dataset(dataset2_files_grouped, [0.8, 0.1, 0.1])

    # Create output directory structure
    create_dir_structure(output_dir, sets, bird_classes)

    # Move dataset1 files to the output directory
    for set_name, files in dataset1_split.items():
        move_files_to_sets(files, output_dir, set_name)

    # Move dataset2 files to the output directory
    for set_name, files in dataset2_split.items():
        move_files_to_sets(files, output_dir, set_name)

merge_datasets(
    dataset1_dir="xeno-canto",
    dataset2_dir="cornel-lab-cleaned",
    output_dir="merged-data"
)
