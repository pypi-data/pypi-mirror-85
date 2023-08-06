from setuptools import setup,find_packages
setup(
    name='TOPSIS_Harshita_101803259',
    version='0.0.2',
    description='implementation of topsis',
    long_description=open('README.txt').read(),
    url='',
    author='harshita',
    author_email='',
    licence='MIT',
    keywords='',
    packages = ["TOPSIS_Harshita_101803259"],
    include_package_data=True,
    install_requires='pandas',
    entry_points={
        "console_scripts": [
            "topsis=TOPSIS_Harshita_101803259:main",
        ]
    },
)