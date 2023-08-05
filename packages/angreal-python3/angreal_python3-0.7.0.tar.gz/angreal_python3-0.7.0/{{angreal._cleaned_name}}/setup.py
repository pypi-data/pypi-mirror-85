import sys
import setuptools
import os



VERSION = open(os.path.join('{{angreal._cleaned_name}}', 'VERSION')).read().strip()




requirements = [
    'click>=7.0.0'
]

dev_requirements = [
'future',
'angreal>=0.7.1',
#Testing
'pytest>=3.8.0',
'pytest-cov>=2.6.0',
#Documentation
'sphinx>=1.8.0',
'sphinx-rtd-theme>=0.4.1',
#Static
'mypy>=0.660',
'lxml>4.3.0',
'setuptools>=39.1.0',
#Linting
'black==19.10b0',
'pre-commit==2.2.0'
]

setuptools.setup(
    name='{{angreal._cleaned_name}}',
    description='',
    long_description='''''',
    url='',
    author='{{angreal.author}}',
    author_email='{{angreal.author_email}}',
    license='GPLv3',
    packages=setuptools.find_packages(),
    install_requires=requirements,
    zip_safe=False,
    version=VERSION,
    entry_points={
        'console_scripts': [
            '{{angreal._cleaned_name}}={{angreal._cleaned_name}}.cli:main'
        ]
    },
    python_requires='>=3.7',
    include_package_data=True,
    extras_require={'dev': dev_requirements}
)
