# Maintainers

When implementation is deemed to be ready for a stable release, ensure the
following steps are performed:

- Update `CHANGELOG.md`, replacing the development title with release
  version and date.
- Ensure the version value in the implementation has been updated.

A release can be made with the following commands.

----

Perform a local clean build:

```shell
python -m build
```

Validate artifacts with a local pip install:

```shell
pip install dist/*.whl
cd <copied-sandbox-example>
python -m tardiff2 --version
pip uninstall tardiff2
```

Create a local release tag and verify the signed tag:

```shell
git tag -s -a v<version> <hash> -m "tardiff2 <version>"
git verify-tag <tag>
```

Push the tag to GitHub to start the release workflow:

```shell
git push origin <tag>
```

After the release workflow creates a build, sanity check its logs to ensure
the generated artifact seems sane. If the package appears to be in a good
state, authorize the workflow's environment to complete publishing.

After a release is made, check the pip install with PyPI:

```shell
cd <copied-sandbox-example>
pip install tardiff2
python -m tardiff2 --version
pip uninstall tardiff2
```

If no issues, complete the automatically created draft release notes in
GitHub to complete the release.
