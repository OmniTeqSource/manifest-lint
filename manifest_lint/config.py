from __future__ import annotations
import re


class LintSettings:
    """The general config for linting. See docstring for more details.
    """

    def __init__(self, allow_multiple=False, skip=False, skip_namespace=False, skip_name=False, ignore=False):
        self._allow_multiple = allow_multiple
        self._skip = skip
        self._skip_namespace = skip_namespace
        self._skip_name = skip_name
        self._ignore = ignore

    @property
    def ignore(self):
        return self._ignore

    @property
    def skip(self):
        return self._skip

    @property
    def skip_namespace(self):
        return self._skip or self._skip_namespace

    @property
    def skip_name(self):
        return self._skip or self._skip_name

    @property
    def allow_multipe(self):
        return self._allow_multiple


class LintConfig:
    def __init__(self):
        self.manifest_line_pattern = re.compile(r'\#\s*manifest-lint:\s*')
        self.pre_manifest_line_pattern = re.compile(
            r'.*(?=\#\s*manifest-lint:)')
        self.csv_pattern = re.compile(r'(.+?)(?:,\s*|$)')

    def _init_settings(self,
                       allow_multiple=False,
                       skip=False,
                       skip_namespace=False,
                       skip_name=False,
                       ignore=False, **_):
        return LintSettings(allow_multiple, skip, skip_namespace, skip_name, ignore)

    def __call__(self,  raw: list[str]):
        """Parses lint comments in a file and builds the settings from it."""
        all_lints = []
        for line in raw:
            line = line.rstrip('\n')
            # no lint detected in line
            if len(self.manifest_line_pattern.findall(line)) == 0:
                continue
            # remove non comments before
            line = self.pre_manifest_line_pattern.sub("", line)
            # extract csv items
            all_lints += self.csv_pattern.findall(
                self.manifest_line_pattern.sub("", line))
        # convert to snek
        all_lints = [x.replace("-", "_") for x in set(all_lints)]

        # all flags are defaulted to false, so convert all flags present in
        # comment to a dict of {"flag1": True} and spread to LintSettings
        return self._init_settings(**dict(zip(all_lints, [True] * len(all_lints))))
