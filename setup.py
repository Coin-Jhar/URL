from setuptools import setup, find_packages

setup(
    name="url-analyzer",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.25.1",
        "beautifulsoup4>=4.9.3",
        "dnspython>=2.1.0",
        "python-whois>=0.7.3",
        "pyOpenSSL>=20.0.1",
    ],
)
