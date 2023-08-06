from setuptools import setup

with open("requirements.txt") as f:
    install_requires = f.readlines()

with open("README.md") as f:
    long_description = f.read()

setup(
    name="uio-monty-hall-game",
    version="2020.11.1",
    author="Simon Funke",
    author_email="simon@simula.no",
    description="A game implementation of the Monty Hall problem.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="BSD",
    packages=["monty_hall_game"],
	package_data={"monty_hall_game": ["templates/**"]},
    install_requires=install_requires,
    scripts=["bin/play_monty_hall_cli.py", "bin/play_monty_hall_web.py"],
    zip_safe=False,
)
