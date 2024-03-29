from setuptools import setup, find_packages

setup(
    name='tim',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'click',
        'colorama',
        'lark'
    ],
    entry_points={
        'console_scripts': [
            'tim = tim.api:tim',
        ],
    },
)
