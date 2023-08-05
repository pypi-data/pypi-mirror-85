from setuptools import setup

with open('README.md') as f:
	readme = f.read()

with open('requirements.txt') as f:
	requirements = f.readlines()

setup(
	name='dpytils',
	version="0.0.4",
	packages=['dpytils'],
	url='https://github.com/TymanWasTaken/dpytils',
	license='MIT License',
	author='Tyman',
	description='A package with all sorts of utilities for discord.py.',
	long_description=readme,
	long_description_content_type="text/markdown",
	project_urls={
		"Issue Tracker": "https://github.com/TymanWasTaken/dpytils/issues",
		"Documentation": "https://github.com/TymanWasTaken/dpytils/wiki"
	},
	install_requires=requirements
)