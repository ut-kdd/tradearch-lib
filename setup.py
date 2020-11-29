from os import path

from setuptools import setup, find_packages

here = path.abspath(path.dirname(__file__))

with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    # region core
    name="tradearch",
    version="0.0.3",
    python_requires=">=3.5",
    packages=find_packages(exclude=["scripts"]),
    install_requires=[
        "joblib==0.17.0; python_version >= '3.6'",
        "numpy==1.19.4",
        "pandas==1.1.4",
        "python-dateutil==2.8.1; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'",
        "pytz==2020.4",
        "scikit-learn==0.23.2",
        "scipy==1.5.4; python_version >= '3.6'",
        "six==1.15.0; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'",
        "ta==0.7.0",
        "threadpoolctl==2.1.0; python_version >= '3.5'",
    ],
    extras_require={
        "dev": [
            "appdirs==1.4.4",
            "attrs==20.3.0; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'",
            "black==19.10b0; python_version >= '3.6'",
            "bleach==3.2.1; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4'",
            "cached-property==1.5.2",
            "cerberus==1.3.2",
            "certifi==2020.11.8",
            "cffi==1.14.4",
            "chardet==3.0.4",
            "click==7.1.2; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4'",
            "colorama==0.4.4; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4'",
            "cryptography==3.2.1; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4'",
            "distlib==0.3.1",
            "docutils==0.16; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4'",
            "idna==2.10; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'",
            "jeepney==0.6.0; sys_platform == 'linux'",
            "keyring==21.5.0; python_version >= '3.6'",
            "orderedmultidict==1.0.1",
            "packaging==20.7; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'",
            "pathspec==0.8.1",
            "pep517==0.9.1",
            "pip-shims==0.5.3; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4'",
            "pipenv-setup==3.1.1",
            "pipfile==0.0.2",
            "pkginfo==1.6.1",
            "plette[validation]==0.2.3; python_version >= '2.6' and python_version not in '3.0, 3.1, 3.2, 3.3'",
            "pycparser==2.20; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'",
            "pygments==2.7.2; python_version >= '3.5'",
            "pyparsing==2.4.7; python_version >= '2.6' and python_version not in '3.0, 3.1, 3.2, 3.3'",
            "python-dateutil==2.8.1; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'",
            "readme-renderer==28.0",
            "regex==2020.11.13",
            "requests==2.25.0; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4'",
            "requests-toolbelt==0.9.1",
            "requirementslib==1.5.16; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4'",
            "rfc3986==1.4.0",
            "secretstorage==3.3.0; sys_platform == 'linux'",
            "six==1.15.0; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'",
            "toml==0.10.2; python_version >= '2.6' and python_version not in '3.0, 3.1, 3.2, 3.3'",
            "tomlkit==0.7.0; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4'",
            "tqdm==4.54.0; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'",
            "twine==3.2.0",
            "typed-ast==1.4.1",
            "urllib3==1.26.2; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4' and python_version < '4'",
            "vistir==0.5.2; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'",
            "webencodings==0.5.1",
            "wheel==0.35.1; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4'",
        ]
    },
    dependency_links=[],
    # endregion
    # region metadata
    description="research-oriented library for market prediction",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ut-kdd/tradearch-lib/",
    author="Mahdi Sadeghi",
    author_email="mail2mahsad@gmail.com",
    project_urls={
        "Bug Reports": "https://github.com/ut-kdd/tradearch-lib/issues",
        "Source": "https://github.com/ut-kdd/tradearch-lib/",
    },
    # endregion
    # region data
    package_data={"tradearch": ["data/*"]},
    # endregion
)
