from setuptools import setup, find_packages

classifiers = [
	'Development Status :: 5 - Production/Stable',
	'Intended Audience :: Education',
	'Operating System :: Microsoft :: Windows :: Windows 10',
	'License :: OSI Approved :: MIT License',
	'Programming Language :: Python :: 3'
]

setup(
	name='drew',
	version='0.0.11',
	description='drew',
	long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
	url='',
	author='Drew Summy',
	author_email='dtsummy@gmail.com',
	license='MIT',
	classifiers=classifiers,
	keywords='',
	packages=find_packages(),
	install_requires=[],
	include_package_data=True
)