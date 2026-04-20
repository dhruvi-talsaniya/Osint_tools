from setuptools import setup, find_packages

setup(
    name='osint-tools',  # Replace with your package name
    version='0.1.0',  # Replace with your package version
    author='Dhruvi Talsaniya',
    author_email='your_email@example.com',  # Replace with your email
    description='A collection of tools for Open Source Intelligence (OSINT) gathering.',
    long_description=open('README.md').read(),  # Assumes a README.md file exists
    long_description_content_type='text/markdown',
    url='https://github.com/dhruvi-talsaniya/Osint_tools',  # Replace with your GitHub repo link
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
        # List your dependencies here
        'requests',
        'beautifulsoup4',
    ],
)