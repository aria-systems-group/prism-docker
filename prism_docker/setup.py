import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="prism_docker_interface",
    version="1.0.0",
    author="Kandai Watanabe, Akash Ratheesh",
    author_email="Kandai.Watanabe@colorado.edu ,Akash.RatheeshBabu@colorado.edu",
    description="A simple interface to use Dockerized PRISM/PRISM-GAMES",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/aria-systems-group/prism-docker",
    project_urls={
        "Bug Tracker": "https://github.com/aria-systems-group/prism-docker/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)