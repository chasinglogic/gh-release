from github_release.git import git
from github_release.version_files.cargo_toml import CargoTOML
from github_release.version_files.dunder_version import DunderVersion
from github_release.version_files.package_json import PackageJSON
from github_release.version_files.pyproject import PyProjectTOML
from github_release.version_files.setup_py import SetupPy

VERSION_FILES = [
    PackageJSON,
    SetupPy,
    PyProjectTOML,
    DunderVersion,
    CargoTOML,
]


def update_version_files(version):
    updated = update_vfs(version)
    if updated:
        git("commit", "-m", f"release: {version}")
        git("push")


def update_vfs(version):
    version_file_updated = False
    for version_file in VERSION_FILES:
        vf = version_file.from_file()
        if not vf:
            continue

        updated = vf.update(str(version))
        if updated:
            print("Updated version in:", vf.filename)

        version_file_updated = version_file_updated or updated

    return version_file_updated
