from setuptools import setup, find_packages

setup(
	name='dynbsp',
	version='0.1',
	author="James Waters",
	author_email="james@jcwaters.co.uk",
	description="An application to dynamically add, remove and rename desktops from the BSP window manager",
	url="https://github.com/j-waters/dynbsp",
	packages=find_packages(),
	include_package_data=True,
	install_requires=['Click', 'PyYAML'],
	entry_points='''
        [console_scripts]
        dynbsp=dynbsp.__main__:cli
    ''',
	python_requires='>=3.8',
)
