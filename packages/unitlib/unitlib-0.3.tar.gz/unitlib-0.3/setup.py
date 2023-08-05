from setuptools import find_packages, setup


GITHUB_URL = "https://github.com/tfiers/unitlib"

with open("ReadMe.md", mode="r", encoding="utf-8") as f:
    readme = f.read()

setup(
    name="unitlib",
    description="📐 Physical units for NumPy arrays ⏱ Fast • Simple • High voltage",
    author="Tomas Fiers",
    author_email="tomas.fiers@gmail.com",
    long_description=readme,
    long_description_content_type="text/markdown",
    url=GITHUB_URL,
    project_urls={"Source Code": GITHUB_URL},
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    packages=find_packages("src"),
    package_dir={"": "src"},  # This means: "Root package can be found in src dir"
    python_requires=">= 3.6",
    #   Why this minimum Python version?
    #   `typing-extensions` (see below) does not provide a backport for
    #   `typing.Protocol` (which we use in `type_aliases.py`) for Python 3.5.
    install_requires=[
        "numpy >= 1.17",  #  `__array_function__` (which we use in `Array`) is
        #                 # introduced in NumPy 1.16, and enabled by default in NumPy
        #                 # 1.17 (namely without the need for setting a special env var).
        #
        # Requirements for older Python versions only:
        "dataclasses; python_version < '3.7'",  # `dataclasses` became part of the
        #                                       # standard library in Python 3.7 only.
        "typing-extensions; python_version < '3.8'",  # Provides backports of eg
        #                                       # `TYPE_CHECKING`, which was not part of
        #                                       # the `typing` module until Python 3.8.
    ],
    # Get package version from git tags
    setup_requires=["setuptools_scm"],
    use_scm_version={
        "version_scheme": "post-release",
        "local_scheme": "dirty-tag",
    },
)
