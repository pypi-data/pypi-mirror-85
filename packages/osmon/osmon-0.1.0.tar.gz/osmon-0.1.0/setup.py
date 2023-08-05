import pathlib  
from setuptools import setup

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setup (

    name='osmon',
    version='0.1.0',
    description='Simple cli system monitor made for fun.',
    long_description=README,
    long_description_content_type='text/markdown',
    url='https://github.com/a1eaiactaest/osmon',
    author='Piotrek Rybiec',
    licence='MIT',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    packages=["osmon"],
    include_package_data=True,
    install_requires=["psutil","argparse","gpuinfo","speedtest-cli"],
    entry_points={
        "console_scripts": [
            "osmon=osmon.__main__:main",
        ]
    },
)
