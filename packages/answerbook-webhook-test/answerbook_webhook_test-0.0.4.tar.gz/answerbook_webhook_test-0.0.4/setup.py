from setuptools import setup, find_packages
from sys import path

from answerbook_webhook_test import __version__

path.insert(0, '.')

NAME = "answerbook_webhook_test"

if __name__ == "__main__":

    with open('requirements.txt') as f:
        requirements = f.read().splitlines()

    setup(
        name=NAME,
        version=__version__,
        author="Jonathan Kelley",
        author_email="jonkelley@gmail.com",
        url="https://github.com/jondkelley/answerbook_webhook_test",
        license='Copyleft',
        packages=find_packages(),
        package_dir={NAME: NAME},
        description="answerbook_webhook_test - Just a simple webhook test app",

        install_requires=requirements,

        entry_points={
            'console_scripts': ['answerbook_webhook_test = answerbook_webhook_test.app:cli'],
        }
    )
