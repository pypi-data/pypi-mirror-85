import setuptools

with open("README.md", "r") as fh:
    LONG_DESCRIPTION = fh.read()

setuptools.setup(
    name="pyxperiment",
    version="0.0.9",
    author="Stanislau Piatrusha",
    author_email="petrushas@gmail.com",
    description="A framework for performing scientific measurements",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url="https://bitbucket.org/petrushas/pyxperiment",
    python_requires='>=3',
    license='MIT License',
    packages=setuptools.find_packages(),
    install_requires=[
        'matplotlib',
        'pyvisa',
        'wxPython',
        'lxml',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
