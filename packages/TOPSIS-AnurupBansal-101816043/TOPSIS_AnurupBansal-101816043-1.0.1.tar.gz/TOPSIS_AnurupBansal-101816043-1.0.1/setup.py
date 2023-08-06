from setuptools import setup

setup(
    name="TOPSIS_AnurupBansal-101816043",
    version="1.0.1",
    description="This is a Python package to implement TOPSIS technique.",
    author="Anurup Bansal",
    author_email="anurupbansal@gmail.com",
    url = 'https://pypi.org/project/TOPSIS-AnurupBansal-101816043',
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        "Programming Language :: Python :: 3.7",
    ],
    packages=["source"],
    include_package_data=True,
    install_requires=['scipy',
                      'tabulate',
                      'numpy',
                      'pandas',
     ],
     entry_points={
        "console_scripts": [
            "topsis=source.topsis:main",
        ]
     },
)
