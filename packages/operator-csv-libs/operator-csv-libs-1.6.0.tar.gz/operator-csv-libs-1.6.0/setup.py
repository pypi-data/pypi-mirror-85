from setuptools import setup, find_packages

setup(
    name='operator-csv-libs',
    version='1.6.0',
    description='Code to manage OLM related CSVs and channels',
    author='bennett-white',
    url='https://github.com/multicloud-ops/operator-csv-libs',
    packages=['operator_csv_libs'],
    install_requires=[
        'pyyaml',
        'pygithub',
        'dohq-artifactory',
        'slack_log_handler',
        'requests'
    ]
)