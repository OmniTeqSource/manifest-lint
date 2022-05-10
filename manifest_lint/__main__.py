import argparse

from .exceptions import ManifestError
from .validate import enforce

parser = argparse.ArgumentParser()
parser.add_argument("--root-dir",  help="Directory to parse and enforce.")

if __name__ == "__main__":
    args = parser.parse_args()
    filename = args.root_dir
    try:
        enforce(filename)
    except Exception as e:
        ManifestError.err(filename, str(e))
    ManifestError.display()
