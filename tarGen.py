import tarfile
import os.path
import sys

def make_tarfile(output_filename, source_dir):
    with tarfile.open(output_filename, "w") as tar:
        tar.add(source_dir, arcname = os.path.basename(source_dir))


if __name__ == "__main__":
    make_tarfile(output_filename=sys.argv[1], source_dir=sys.argv[2])