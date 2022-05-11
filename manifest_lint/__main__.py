import argparse

from .exceptions import ManifestError
from .validate import enforce

parser = argparse.ArgumentParser()
parser.add_argument("--root-dir",  help="Directory to parse and enforce.")
parser.add_argument("--skip-namespace",
                    help="Skips namespace", action="store_true")
parser.add_argument("--skip-namespace-gh-action",
                    help="Skips namespace but string arg because GitHub actions doesn't support flags.", type=str, default="false")
parser.add_argument("--skip-name",
                    help="Skips name", action="store_true")
parser.add_argument("--skip-name-gh-action",
                    help="Skips names but string arg because GitHub actions doesn't support flags.", type=str, default="false")
parser.add_argument("--skip",
                    help="Skips namespace and name", action="store_true")
parser.add_argument("--skip-gh-action",
                    help="Skips namespace and name but string arg because GitHub actions doesn't support flags.", type=str, default="false")
parser.add_argument("--ignore", help="Ignore all", action="store_true")
parser.add_argument("--ignore-gh-action",
                    help="Ignore all but string arg because GitHub actions doesn't support flags.", type=str, default="false")
parser.add_argument("--allow-multiple",
                    help="Allow multiple flag", action="store_true")
parser.add_argument("--allow-multiple-gh-action",
                    help="Allow multiple flag but string arg because GitHub actions doesn't support flags.", type=str, default="false")


if __name__ == "__main__":
    args = parser.parse_args()

    enforce(**{
        "root_dir": args.root_dir,
        "skip_namespace": args.skip_namespace or (args.skip_namespace_gh_action.lower() == "true"),
        "skip_name": args.skip_name or (args.skip_name_gh_action.lower() == "true"),
        "skip": args.skip or (args.skip_gh_action.lower() == "true"),
        "ignore": args.ignore or (args.ignore_gh_action.lower() == "true"),
        "allow_multiple": args.allow_multiple or (args.allow_multiple_gh_action.lower() == "true"),
    })
    ManifestError.display()
