import sys
from setuptools import setup, Command

if sys.version_info[0] != 3:
    print('Stoffel requires Python 3 to run.')
    sys.exit(1)

setup(
    name='Stoffel',
    version="0.1.1",
    description="A tool to connect Excel/Sheets to Powerpoint/Slides.",
    author='Nathan Duncan',
    author_email='nduncan@fifthpartners.com',
    url='https://github.com/fifth-partners/stoffel',
    license='LGPLv3',
    python_requires="!=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*",
    install_requires=[
        "xlwings==0.20.8", 
        "datetime==4.3",
        "google-api-python-client==1.12.5",
        "google-auth-httplib2==0.0.4",
        "google-auth-oauthlib==0.4.1",
        "PyDrive==1.3.1",
        "tabulate==0.8.7",
        "flask==1.1.2",
        "pillow==8.0.1",
    ],
    download_url = 'https://github.com/fifth-partners/stoffel/archive/v0.1.1.zip',
    include_package_data=True, 
    packages=['stoffel'],
    entry_points={"console_scripts": ["stoffel=stoffel.__main__:main"]},
    classifiers=[
        'Intended Audience :: Developers',
    ]
)