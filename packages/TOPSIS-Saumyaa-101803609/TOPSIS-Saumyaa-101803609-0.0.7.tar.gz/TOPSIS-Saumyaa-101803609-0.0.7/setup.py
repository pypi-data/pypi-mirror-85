import setuptools
def readme():
    with open('README.md', encoding='utf8') as f:
        README =f.read()
    return README
setuptools.setup(
    name="TOPSIS-Saumyaa-101803609",
    version="0.0.7",
    author="Saumyaa Mathur",
    author_email="saumyaamathur27@gmail.com",
    description="topsis package",
    long_description= readme(),
    long_description_content_type="text/markdown",
    license="MIT",
    url="https://github.com/pypa/sampleproject",
    packages=['topsis_py'],
    install_requires=['pandas','statistics'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    entry_points={
        "console_scripts": [
            "topsis=topsis_py.topsis:topsis",
            "topsis_cmd=topsis_py.topsis_cmd"
        ]
    },
)