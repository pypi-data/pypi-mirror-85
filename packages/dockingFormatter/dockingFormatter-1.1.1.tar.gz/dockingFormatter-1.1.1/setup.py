from setuptools import setup

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='dockingFormatter',
    version='1.1.1',
    description='A docking logs formatter',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/LSWarss/dockingFormatter',
    author='Łukasz Stachnik',
    author_email='ls.warss98@gmail.com',
    license='MIT License',
    install_requires=['openpyxl','Click'],
    extras_require = {
        "dev" : [
            "pytest>=6.0",
        ],
    },
    py_modules=['formatter', 'dockingFormatter'],
    package_dir={'':'src'},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
    entry_points='''
        [console_scripts]
        dockingFormatter=dockingFormatter:run
    ''',
)

