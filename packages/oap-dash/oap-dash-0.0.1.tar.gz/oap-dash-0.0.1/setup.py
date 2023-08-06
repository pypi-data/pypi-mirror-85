import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

def read_req_file(req_type):
    with open("requires-{}.txt".format(req_type)) as fp:
        requires = (line.strip() for line in fp)
        return [req for req in requires if req and not req.startswith("#")]

setuptools.setup(
    name="oap-dash",
    version="0.0.1",
    author="Donald Lafranchi",
    author_email="it.corridor051@gmail.com",
    description="Customized Dash for OpsRamp Reports",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=read_req_file("install"),
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)