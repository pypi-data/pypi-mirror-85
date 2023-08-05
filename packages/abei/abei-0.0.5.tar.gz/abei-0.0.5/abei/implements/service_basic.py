import subprocess
import sys


def install_packages(package_names):
    for package in (package_names or []):
        subprocess.call([sys.executable, '-m', 'pip', 'install', package])


class ServiceBasic(object):

    @classmethod
    def ensure_dependencies(cls):
        install_packages(cls.get_dependencies())

    @classmethod
    def get_dependencies(cls):
        return []
