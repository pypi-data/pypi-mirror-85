from setuptools import setup, find_packages


def readme():
	with open('./README.md') as f:
		return f.read()


setup(
	name='ceramic',
	version='2020.11.12',
	license='MIT',
	url='https://github.com/idin/ceramic',
	author='Idin',
	author_email='py@idin.ca',
	description='Python library for defining data tables as tiles',
	long_description=readme(),
	long_description_content_type='text/markdown',
	classifiers=[
		'Development Status :: 3 - Alpha',
		'Intended Audience :: Developers',
		'Programming Language :: Python :: 3 :: Only',
		'Programming Language :: Python :: 3.6',
		'Programming Language :: Python :: 3.7',
		'Topic :: Software Development :: Libraries :: Python Modules'
	],
	packages=find_packages(exclude=["jupyter_tests", ".idea", ".git"]),
	install_requires=[
		'sklearn', 'pandas', 'joblib',
		'ravenclaw', 'chronometry', 'nightingale', 'pensieve', 'slytherin'
	],
	python_requires='~=3.6',
	zip_safe=False
)
