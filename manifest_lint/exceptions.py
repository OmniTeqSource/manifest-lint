
class ManifestError:
    messages = []
    """Validation errors"""

    @classmethod
    def err(cls, filename: str, reason: str):
        ManifestError.messages.append((filename, reason))
        return cls()

    @staticmethod
    def multiple(filename: str):
        ManifestError.err(filename, "multiple manifests per file")

    @staticmethod
    def leading(filename: str):
        ManifestError.err(filename, "kind should be leading in filename")

    @staticmethod
    def no_name(filename: str):
        ManifestError.err(filename, "manifest name should be in filename")

    @staticmethod
    def no_namespace(filename: str):
        ManifestError.err(filename, "manifest namespace should be in filename")

    @staticmethod
    def empty(filename: str):
        ManifestError.err(filename, "empty manifest")

    @staticmethod
    def mulitple_same(filename: str):
        ManifestError.err(
            filename, "all manifests in a file must be same apiVersion and kind")

    @staticmethod
    def pattern(filename: str):
        ManifestError.err(
            filename, "YAML filename should follow pattern `[a-z]+(-[a-z0-9])+.(yaml|yml)$`")

    @staticmethod
    def display():
        for filename, reason in ManifestError.messages:
            print(f"::error file={filename}::{reason}")
