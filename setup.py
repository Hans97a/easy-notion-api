import setuptools


with open("README.md", "r", encoding="utf-8") as file:
    long_description = file.read()


def get_requirements() -> list:
    """get required libs from file"""
    with open("requirements.txt", "r", encoding="utf-8") as file:
        requirements = list()
        for lib in file.read().split("\n"):
            if not lib.startswith("-") or lib.startswith("#"):
                requirements.append(lib.strip())
        return requirements


setuptools.setup(
    name="easy-notion-api",
    version="0.1.3",
    author="Hans97a",
    author_email="byby8992@naver.com",
    description="Unofficial Python API client for Notion",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Hans97a/easy-notion-api",
    install_requires=get_requirements(),
    include_package_data=True,
    packages=setuptools.find_packages(include=["notion", "notion.*"]),
    python_requires=">=3.11",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
