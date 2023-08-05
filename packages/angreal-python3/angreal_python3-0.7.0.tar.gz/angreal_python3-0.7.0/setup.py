import setuptools
import os
import sys
from pathlib import Path


VERSION = open(os.path.join('VERSION')).read().strip()
py_version_tag = '-%s.%s'.format(sys.version_info[:2])
if not sys.version_info >= (3, 0):
    print('Python 3 is required', file=sys.stderr)
    exit(1)


NAME = 'angreal_python3'
DESCRIPTION='An angreal template for python3 projects'
LONG_DESCRIPTION=open('README.rst').read()
AUTHOR='dylanbstorey'
AUTHOR_EMAIL='dylan.storey@gmail.com'
URL='https://gitlab.com/angreal/angreal_python3'
FILES_TO_COPY = [
    '{{angreal._cleaned_name}}',
    'angreal.json'
    ]



# SHOULDNT NEED TO GO BELOW THIS LINE

def generate_data_files(*args):
    """
    generate data_files parameter for setup tools

    takes files and directories to be added.

    :param args:
    :return:
    """


    sys_exe = Path(sys.executable)
    data_files = []

    def package_files(directory):
        """
        get all the files in a directory

        :param directory:
        :return:
        """
        paths = []
        for (path, directories, filenames) in os.walk(directory):
            for filename in filenames:
                paths.append(os.path.join(path, filename))
        return paths

    for path in args:
        if os.path.isfile(path):
            data_files.append( ( NAME , [path]) )
        elif os.path.isdir(path):
            for p in package_files(path):
                data_files.append( ( os.path.dirname(os.path.join(NAME,p)), [p]) )


    return data_files


setuptools.setup(
    name=NAME,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    url=URL,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    license='GPLv3',
    zip_safe=False,
    version=VERSION,
    python_requires='>=3',
    data_files=generate_data_files(*FILES_TO_COPY),
)