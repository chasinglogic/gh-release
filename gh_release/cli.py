#!/usr/bin/env python3

import argparse
from subprocess import check_output

import requests


def git(*args):
    cmd = ["git"]
    cmd.extend(args)
    return check_output(cmd).decode("utf-8")


def get_repo():
    remotes = check_output(["git", "remote", "-v"]).decode("utf-8").split("\n")
    for remote in remotes:
        if not remote:
            continue

        first_segment, _ = remote.split(" ")
        _, url = first_segment.split("\t")

        if "github.com" not in url:
            continue

        if url.startswith("ssh") or url.startswith("git@"):
            return url.split(":")[-1]
        else:
            return "/".join(url.split("/")[-2:])


def get_last_version():
    versions = [
        Version.from_str(ver[len("refs/tags/") :])
        for ver in (
            check_output(
                [
                    "git",
                    "for-each-ref",
                    "--sort=-taggerdate",
                    "--format",
                    "%(refname)",
                    "refs/tags",
                ]
            )
            .decode("utf-8")
            .split("\n")
        )
        if ver[len("refs/tags/") :]
    ]
    if not versions:
        return Version(0, 0, 0)

    return sorted(versions)[-1]


def get_commit_for_tag(tag):
    return (
        check_output(["git", "show", "--no-patch", "--pretty=%H", tag])
        .decode("utf-8")
        .strip()
    )


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
        default=get_repo(),
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

    last_version = get_last_version()
    if last_version == Version(0, 0, 0):
        commits = git("log", "--reverse", "--format=%H").split("\n")
        # Initial commit to the branch / repository
        last_version_commit = commits[0]
    else:
        last_version_commit = get_commit_for_tag(str(last_version))

    version_commit = get_commit_for_tag("HEAD")

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

    messages = check_output(
        [
            "git",
            "log",
            "--pretty=format:%h %s",
            f"{last_version_commit}...{version_commit}",
        ],
    ).decode("utf-8")
    changelog = "\n".join(
        [
            f"- {message}"
            for message in messages.split("\n")
            if message
            and "release: " not in message
            and "Merge pull request" not in message
        ],
    )

    emails = check_output(
        [
            "git",
            "log",
            "--pretty=format:%an <%ae>",
            f"{last_version_commit}...{version_commit}",
        ],
    ).decode("utf-8")
    contributors = "\n".join({f"- {email}" for email in emails.split("\n") if email})

    if args.title:
        release_notes = f"# Release {version}\n\n"
    else:
        release_notes = ""

    release_notes += (
        f"{changelog}\n\n## Contributors to this Release\n\n{contributors}\n"
    )

    body = {
        "tag_name": str(version),
        "name": str(version),
        "body": release_notes,
        "draft": args.draft,
        "prerelease": args.pre_release,
    }

    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
    }

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

    version_file_updated = False
    for version_file in []:
        vf = version_file.from_file()
        if not vf:
            continue

        version_file_updated = vf.update(str(version))
        if version_file_updated:
            print("Updated version in:", vf.filename)

    if version_file_updated:
        git("add", "package.json")
        git("commit", "-m", f"release: {version}")
        git("push")

    git("tag", str(version))
    git("push", "--tags")
    response = requests.post(
        f"https://api.github.com/repos/{args.repo}/releases",
        headers=headers,
        json=body,
    )
    try:
        response.raise_for_status()
    except Exception as exc:
        print("Failed to create release!")
        print(exc)
        print(f"{response.text}")


if __name__ == "__main__":
    main()
