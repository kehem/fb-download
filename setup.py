from setuptools import setup, find_packages

setup(
    name='fb-video',
    version='0.1.3',
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
    entry_points={
        'console_scripts': [
            'fb-scraper = fb_video.fb:main',  # Updated to fb_video.fb
        ],
    },
    author='Kehem IT',
    author_email='support@kehem.com',
    description='A Facebook video information scraper by Kehem IT',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/kehem/fb-download',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)