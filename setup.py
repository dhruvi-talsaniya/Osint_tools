from setuptools import setup, find_packages

setup(
    name="osint-tools",
    version="1.0.0",
    author="Dhruvi Talsaniya",
    author_email="your_email@example.com",
    description="A comprehensive toolkit for Open Source Intelligence (OSINT) gathering.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/dhruvi-talsaniya/Osint_tools",
    project_urls={
        "Bug Tracker": "https://github.com/dhruvi-talsaniya/Osint_tools/issues",
        "Source": "https://github.com/dhruvi-talsaniya/Osint_tools",
    },
    packages=find_packages(exclude=["tests*"]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Security",
        "Topic :: Internet",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
    ],
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.28",
        "beautifulsoup4>=4.11",
        "python-whois>=0.8",
        "dnspython>=2.2",
        "click>=8.0",
        "python-dotenv>=1.0",
        "PyYAML>=6.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0",
            "pytest-cov>=4.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "osint-tools=osint_tools.cli:cli",
        ],
    },
    include_package_data=True,
)
