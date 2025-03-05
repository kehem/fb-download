from setuptools import setup, find_packages

setup(
    name='facebook-scraper',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
    entry_points={
        'console_scripts': [
            'fb-scraper = facebook_scraper.fb:main',
        ],
    },
    author='Kehem IT',
    author_email='support@kehem.com',
    description='A Facebook video information scraper by Kehem IT',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/facebook-scraper',  # Optional
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)