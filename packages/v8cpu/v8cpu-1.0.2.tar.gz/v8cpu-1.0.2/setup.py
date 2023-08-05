import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="v8cpu",
    version="1.0.2",
    author="Yue Qin",
    author_email="747929791@qq.com",
    description="V8-CPU simulator of J. Glenn Brookshear’s book - 'Computer Science An Overview', Appendix C.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/747929791/v8cpu",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)