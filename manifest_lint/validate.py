import os
import re
import yaml

from .config import LintSettings, LintConfig
from .exceptions import ManifestError


KEBAB_PATTERN = re.compile(r'(?<!^)(?=[A-Z])')
FNAME_PATTERN = re.compile(r'^[a-z]+(-[a-z0-9]+){0,4}.yaml$')


def lstrip(s, t):
    """lstrip exactly"""
    return s[len(t):]


class ManifestParser:
    def __init__(self, raw: dict):
        self._kind = raw["kind"]
        self._apiVersion = raw["apiVersion"]
        self._metadata = raw.get("metadata", {})

    @property
    def kind_kebab(self):
        if self.is_flux and self.is_flux_kustomization:
            return "kustomization-flux"
        return KEBAB_PATTERN.sub('-', self._kind).lower()

    @property
    def is_flux(self):
        return "fluxcd.io" in self._apiVersion

    @property
    def is_namespace(self):
        return self._kind == "Namespace"

    @property
    def is_kustomization(self):
        return self._kind == "Kustomization" and not self.is_flux

    @property
    def is_flux_kustomization(self):
        return self._kind == "Kustomization" and self.is_flux

    @property
    def name(self):
        return self._metadata.get("name")

    @property
    def namespace(self):
        return self._metadata.get("namespace")

    @property
    def should_have_namespace(self):
        return not (self.is_namespace or self.is_kustomization or self.is_flux_kustomization)

    @property
    def should_have_name(self):
        return not (self.is_namespace or self.is_kustomization or self.is_flux_kustomization)


def validate_manifest(settings: LintSettings, filename: str, raw: dict):
    """Validates manifest based on naming structure"""

    name = os.path.basename(filename).replace(
        ".yaml", "").replace(".yml", "").lower()
    manifest = ManifestParser(raw)

    # Match Kind
    if not name.startswith(manifest.kind_kebab):
        return ManifestError.leading(filename)
    else:
        name = lstrip(name, manifest.kind_kebab)

    # Match namespace
    if name.startswith("-"):
        name = lstrip(name, "-")

    if manifest.should_have_namespace and not settings.skip_namespace:
        if manifest.namespace is None or not name.startswith(manifest.namespace):
            return ManifestError.no_namespace(filename)

        name = lstrip(name, manifest.namespace)
        if name.startswith("-"):
            name = lstrip(name, "-")
    # Match name
    if manifest.should_have_name and not settings.skip_name:
        if manifest.name is None or not name.startswith(manifest.name):
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
    validate_manifest(settings, filename, data[0])


def enforce(root_dir: str, **kwargs):
    """Enforces a directory"""
    config = LintConfig(**kwargs)
    for (dirpath, _, filenames) in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith(('.yml', '.yaml')):
                if FNAME_PATTERN.match(filename) is None:
                    ManifestError.pattern(filename)
                filename = os.path.join(dirpath, filename)
                try:
                    check_file(config, filename)
                except Exception as e:
                    ManifestError.err(filename, str(e))
