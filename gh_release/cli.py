#!/usr/bin/env python3

import argparse
import os
import sys
from copy import deepcopy

from gh_release.git import get_commit_for_tag, get_repo, git
from gh_release.github import create_release
from gh_release.release import release_notes_for_version
from gh_release.version import Version
from gh_release.version_files import update_version_files


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--version",
        "-v",
        type=str,
        default="",
        help="Specify the version to go to",
    )
    parser.add_argument(
        "--pre-release",
        "-l",
        action="store_true",
        help="Indicates this is a pre-release",
    )
    parser.add_argument(
        "--draft",
        "-d",
        action="store_true",
        help="Indicates this is a draft release",
    )
    parser.add_argument(
        "--repo",
        "-r",
        type=str,
        default=None,
        help="The repository to create the release on in :owner/:repo format, "
        "will attempt to parse from git remotes if not given",
    )
    parser.add_argument(
        "--title",
        "-t",
        action="store_true",
        help="If given use the release name as the markdown title, otherwise title "
        "is omitted for Github style formatting",
    )
    parser.add_argument(
        "--minor",
        "-m",
        action="store_true",
        help="Bump by minor",
    )
    parser.add_argument(
        "--major",
        "-j",
        action="store_true",
        help="Bump by major",
    )
    parser.add_argument(
        "--patch",
        "-p",
        action="store_true",
        help="Bump by patch",
    )
    args = parser.parse_args()

    if not any((args.patch, args.minor, args.major, args.version)):
        print("Must provide one of --version, --major, --minor, or --patch.")
        sys.exit(1)

    token = os.getenv("GITHUB_TOKEN")
    if not token:
        print("$GITHUB_TOKEN must be set.")
        sys.exit(1)

    last_version_commit, last_version = Version.latest_version()
    if args.version:
        version = Version.from_str(args.version)
    else:
        version = deepcopy(last_version)
        if args.patch:
            version.increment_patch()
        if args.minor:
            version.increment_minor()
        if args.major:
            version.increment_major()

    version_commit = get_commit_for_tag("HEAD")
    release_notes = release_notes_for_version(
        version,
        version_commit,
        last_version_commit,
    )

    repo = args.repo or get_repo()

    print("Creating release", version, version_commit)
    print("Previous version", last_version, last_version_commit)
    print("Pre-release?", args.pre_release)
    print("Draft release?", args.draft)
    print("Repository", args.repo)
    print("============= Release Notes ============")
    print(release_notes)

    ans = input("Does this look correct? (y/N) ")
    if not ans.startswith("y"):
        return

    if not args.skip_version_files:
        update_version_files(version)

    git("tag", str(version))
    git("push", "--tags")

    try:
        create_release(
            token=token,
            repo=repo,
            tag_name=str(version),
            name=str(version),
            body=release_notes,
            draft=args.draft,
            prerelease=args.prerelease,
        )
    except Exception as exc:
        print("Failed to create release!")
        print(exc)


if __name__ == "__main__":
    main()
