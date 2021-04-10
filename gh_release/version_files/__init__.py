from version_files.cargo_toml import CargoTOML
from version_files.dunder_version import DunderVersion
from version_files.package_json import PackageJSON
from version_files.setup_py import SetupPy

VERSION_FILES = [
    PackageJSON,
    SetupPy,
    DunderVersion,
    CargoTOML,
]
