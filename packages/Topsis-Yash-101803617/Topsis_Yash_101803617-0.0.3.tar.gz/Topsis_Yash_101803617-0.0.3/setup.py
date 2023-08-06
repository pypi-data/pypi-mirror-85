from setuptools import setup

setup(
    name="Topsis_Yash_101803617",
    version="0.0.3",
    description="A Python package implementing TOPSIS technique.",
    author="Yash Shukla",
    author_email="yash981815@gmail.comm",
    url='https://pypi.org/project/Topsis-Yash-101803617/0.0.1/',
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        "Programming Language :: Python :: 3.7",
    ],
    packages=["Topsis_Yash_101803617"],
    include_package_data=True,
    install_requires=['scipy',
                      'tabulate',
                      'numpy',
                      'pandas',
                      ]
)