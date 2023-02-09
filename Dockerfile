FROM ghcr.io/skyfjell/manifest-lint:manifest-lint-0.2.0

ENTRYPOINT [ "python", "-m", "manifest_lint" ]