# release-mgr

A simple tool for managing software releases on GitHub.

This is a polyglot tool, so it aims to supports all kinds of Version metadata files for
all languages. I've added the ones that I use every day but feel free to send a PR with
the version file for your favourite programming language.

## Installation

`release-mgr` is available on pypi:

```
pip3 install --user release_mgr
```

## Usage

```
Usage: release-mgr [OPTIONS]

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

  --skip-upload             Don't try to create a release on github and don't
                            push the commits

  --help                    Show this message and exit.

```

## Example run

```
chasinglogic@raza ~/Code/release-mgr master λ release-mgr --patch
Creating release 0.1.2 8cc48996b099bdb4d2e04e6eeb7a2598381baf68
Previous version 0.1.1 0076879f4ca72a5e30a023c5f83dbcbb34a62f58
Pre-release? False
Draft release? False
Repository chasinglogic/gh-release
============= Release Notes ============
# Release 0.1.2

- 8cc4899 fix: Return True if **any** version file is updated
- 5473ff9 fix: git/ssh urls end with .git
- 429e675 fix: Stage the version file when updated

# Contributors to this Release

- Mathew Robinson <mathew@chasinglogic.io>

Does this look correct? (y/N) y
Updated version in: pyproject.toml
Enumerating objects: 5, done.
Counting objects: 100% (5/5), done.
Delta compression using up to 12 threads
Compressing objects: 100% (3/3), done.
Writing objects: 100% (3/3), 298 bytes | 298.00 KiB/s, done.
Total 3 (delta 2), reused 0 (delta 0), pack-reused 0
remote: Resolving deltas: 100% (2/2), completed with 2 local objects.
To github.com:chasinglogic/release_mgr.git
   8cc4899..4e89ce6  master -> master
Total 0 (delta 0), reused 0 (delta 0), pack-reused 0
To github.com:chasinglogic/release_mgr.git
 * [new tag]         0.1.2 -> 0.1.2
```
