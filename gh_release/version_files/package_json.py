import json

from gh_release.version_files.version_file import VersionFile


class PackageJSON(VersionFile):
    filename = "package.json"

    def update(self, version: str):
        with open("package.json") as pkg_json_file:
            pkg_json = json.loads(pkg_json_file.read())
            pkg_json["version"] = version

        with open("package.json", "w") as pkg_json_file:
            json.dump(
                pkg_json,
                pkg_json_file,
                indent=2,
            )
        return True
