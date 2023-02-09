# Manifest Lint action

Enforces manifest naming for a flux git repository

Rules:

- `allow-multiple` - Allows multiple manifests per file
- `ignore` - Skips file entirely
- `skip` - Skips naming conventions below all together, just enforces `kind` in filename
- `skip-namespace` - Skips namespace enforcement in filename (will ignore `kind: Namespace`)
- `skip-name` - Skips name enforcement in filename

## Examples in yaml

`pod-something.yaml`

```yaml
# manifest-lint: skip-namespace
---
kind: Pod
api: v1
metadata:
  name: something
spec: {}
```

## Inputs

## `directory`

**Required** Directory to run on

## Example usage

```yaml
- name: Manifest Lint
  uses: skyfjell/manifest-lint@0.2.0
  with:
    directory: "test/"
```
