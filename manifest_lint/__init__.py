__doc__ = """\
    Runs naive linting on Kubernetes manifests.

    Rules:
        `allow-multiple` - Allows multiple manifests per file
        `ignore` - Skips file entirely
        `skip` - Skips naming conventions below all together, just enforces `kind` in filename
        `skip-namespace` - Skips namespace enforcement in filename (will ignore `kind: Namespace`)
        `skip-name` - Skips name enforcement in filename

    Examples
    ```yaml
    # manifest-lint: skip-name, allow-multiple
    ---
    kind: Namespace
    api: v1
    metadata:
        name: something
    ```
        
"""