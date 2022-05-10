import os
import re
import yaml

from .config import LintSettings, LintConfig
from .exceptions import ManifestError


KEBAB_PATTERN = re.compile(r'(?<!^)(?=[A-Z])')
FNAME_PATTERN = re.compile(r'^[a-z]+(-[a-z0-9]+){0,2}.yaml$')


def validate_manifest(settings: LintSettings, filename: str, kind="", metadata={}, apiVersion="", **_):
    """Validates manifest based on naming structure"""
    kind_kebab = KEBAB_PATTERN.sub('-', kind).lower()
    name = os.path.basename(filename).rstrip(".yaml").rstrip(".yml").lower()
    is_flux = "fluxcd.io" in apiVersion

    if kind_kebab == "kustomization" and is_flux:
        kind_kebab = "kustomization-flux"

    is_self_named = (kind == "Namespace") or (
        kind == "Kustomization" and not is_flux)

    manifest_name = metadata["name"]
    manifest_namespace = metadata.get("namespace")

    # Match Kind
    if not name.startswith(kind_kebab):
        return ManifestError.leading(filename)
    else:
        name = name.lstrip(kind_kebab)

    # Match namespace
    if name.startswith("-"):
        name = name.lstrip("-")

    if not is_self_named and manifest_namespace and not settings.skip_namespace:
        if not name.startswith(manifest_namespace):
            return ManifestError.no_namespace(filename)

        name = name.lstrip(manifest_namespace)
        if name.startswith("-"):
            name = name.lstrip("-")
    # Match name
    if not is_self_named and not name.startswith(manifest_name) and not settings.skip_name:
        return ManifestError.no_name(filename)


def check_file(config: LintConfig, filename: str):
    """Runs an entire file, breaking into individual manifests"""
    with open(filename) as f:
        raw = f.readlines()
        settings = config(raw)
        f.seek(0)
        raw = f.read()

    if settings.ignore:
        return
    try:
        data = list(yaml.safe_load_all(raw))
    except Exception as e:
        return ManifestError.err(filename, str(e))

    if len(data) == 0:
        return ManifestError.empty(filename)

    if len(data) > 1:
        if not settings.allow_multiple:
            return ManifestError.multiple(filename)
        else:
            if len(set([d["kind"] for d in data])) != 1 or len(set([d["apiVersion"] for d in data])) != 1:
                return ManifestError.mulitple_same(filename)

    # taking first manifest as filename
    validate_manifest(settings, filename, **data[0])


def enforce(root: str):
    """Enforces a directory"""
    config = LintConfig()
    for (dirpath, _, filenames) in os.walk(root):
        for filename in filenames:
            if filename.endswith(('.yml', '.yaml')):
                if FNAME_PATTERN.match(filename) is None:
                    ManifestError.pattern(filename)
                filename = os.path.join(dirpath, filename)
                check_file(config, filename)
