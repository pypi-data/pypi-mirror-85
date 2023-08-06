from setuptools import setup


def readme():
    with open('README.md') as file:
        README = file.read()
    return README


setup(
    name="TOPSIS_Yashika_401803010",
    version="1.0.1",
    description="A Python package implementing TOPSIS technique.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    author="Yashika Katyal",
    author_email="katyal.yashika1999@gmail.com",
    url='https://pypi.org/project/TOPSIS-Yashika-401803010/1.0.0/',
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        "Programming Language :: Python :: 3.7",
    ],
    packages=["src"],
    include_package_data=True,
    install_requires=['scipy',
                      'tabulate',
                      'numpy',
                      'pandas',
                      ],
    entry_points={
        "console_scripts": [
            "topsis=src.topsis:main",
        ]
    },
)
