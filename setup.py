from setuptools import setup, find_packages

setup(
    name='kiki_on_hadoop',
    version='0.1.dev',
    packages=find_packages(),
    install_requires=[
        'mrjob',
        'sqlalchemy',
        'MySQL-python'
    ],
    test_suite='tests',
    entry_points = {
        'console_scripts': [
            'run_kiki = kiki_on_hadoop.run_kiki:main'
        ]
    }
)