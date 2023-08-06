import setuptools

with open("README.rst", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyosmapi",
    version="0.0.1",
    author="jonycoo",
    author_email="jonathan.koehler.7@web.de",
    description="Open Street Map API Wrapper in Python",
    keywords='osm, openstreetmap, wrapper, api',
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/jonycoo/py-osmapi",
    packages=setuptools.find_packages(),
    license='MIT',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
          'requests'
      ],
    python_requires='>=3.6',
)
