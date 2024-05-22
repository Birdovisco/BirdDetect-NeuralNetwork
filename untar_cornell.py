import tarfile

def untar_files(path_to_archive, target_dir):
    with tarfile.open(path_to_archive, 'r') as archive:
        archive.extractall(path=target_dir)

archive_path = 'data/Simon.tar'
target_dir = 'data/cornel-lab/recordings'

untar_files(archive_path, target_dir)
