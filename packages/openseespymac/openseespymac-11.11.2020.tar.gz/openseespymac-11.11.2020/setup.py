import setuptools

about = {}
with open('version.py') as fp:
    exec(fp.read(), about)

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="openseespymac",
    version=about['version'],
    author="Dr. Stevan Gavrilovic",
    author_email="gavrilovic@berkeley.com",
    description="The Mac OS version of OpenSeesPy",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    package_data={
        '': [
            'opensees.so',
            'opensees.pyd',
            'Python',
            'LICENSE.rst',
            '*.so',
            '*.dll',
            '*.dylib',
            '*.so.*'],
    },
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: MacOS :: MacOS X",
    ],
    python_requires='>=3.8',
)
