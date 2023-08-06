#!/usr/bin/python3
from distutils.core import setup
from distutils.command.install	import install

class CmdInstall(install):
	def run(self):
		from distutils.spawn import find_executable, spawn
		import os
		spawn(cmd=('./linux-remote-setup', 'install'))
		install.run(self)


setup(
    name='linux-remote',
    version='3.0.0',
    author='Madhusudhan Kasula',
    author_email='kasula.madhusudhan@gmail.com',
    description='Server for LinuxRemote Android App',
    long_description=open('README.rst').read(),
	url='https://play.google.com/store/apps/details?id=org.linuxremote.app',
	data_files=[
		('bin', ['linux-remote-setup']),
	],
	cmdclass={
		'install': CmdInstall,
	},
	classifiers=[
		'Programming Language :: C',
		'Programming Language :: Python :: 2',
		'Programming Language :: Python :: 3',
		'Operating System :: POSIX :: Linux',
		'Environment :: Console',
	],
)
