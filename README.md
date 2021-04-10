# gh-release

A simple tool for managing software releases on GitHub.

This is a polyglot tool, so it aims to supports all kinds of Version metadata files for
all languages. I've added the ones that I use every day but feel free to send a PR with
the version file for your favourite programming language.

## Usage

```
Usage: gh-release [OPTIONS]

  A simple tool for managing software releases on GitHub.

Options:
  -v, --version TEXT        Specify the version to go to
  -l, --pre-release         Indicates this is a pre-release
  -d, --draft               Indicates this is a draft release
  -r, --repo TEXT           The repository to create the release on in
                            :owner/:repo format, will attempt to parse from
                            git remotes if not given

  -t, --title               If given use the release name as the markdown
                            title, otherwise title is omitted for Github style
                            formatting

  -m, --minor               Bump minor version
  -j, --major               Bump major version
  -p, --patch               Bump patch version
  -s, --skip-version-files  Don't try to update version metadata files
                            (package.json, setup.py etc.)

  --help                    Show this message and exit.
```
