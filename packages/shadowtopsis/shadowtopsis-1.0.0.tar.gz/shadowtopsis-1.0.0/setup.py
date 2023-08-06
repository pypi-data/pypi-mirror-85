from setuptools import setup
import pathlib

#with open("README.md", "r") as fh:
#    long_description = fh.read()
HERE = pathlib.Path(__file__).parent
README=(HERE/'README.md').read_text()
setup(
    name="shadowtopsis", # Replace with your own username
    version="1.0.0",
    author="Devesh Saxena",
    author_email="dsaxena_be18@thapar.edu",
    description="Calculates topsis score",
    long_description=README,
    long_description_content_type="text/markdown",
    #url="https://github.com/pypa/sampleproject",
    license='MIT',
    packages=["topsis"],

    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    include_package_data=True,
    install_requires=['pandas'],
    entry_points={
    "console_scripts":["shatop=topsis.__main__:main",
                       ]
    },
)
