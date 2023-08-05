import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="nsosurveytools",
    version="1.4",
    description=" Tools To Save Time ",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/superuser789/surveytools/",
    author="Nitin Singh",
    author_email="acc4nitin@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["nsosurveytools"],
    #include_package_data=True,
    package_data = {
        # If any package contains *.txt or *.rst files, include them:
        '': ['*.txt', '*.xml', '*.special', '*.pkl'],
    },
    entry_points={
    'console_scripts': [
        'agriculturesurvey = nsosurveytools.agrisurvey:agriculturesurvey',
        'agriplotcmd = nsosurveytools.agrisurvey:agriplotcmd',
        'selectplotscmd = nsosurveytools.agrisurvey:selectplotscmd',
        'getsubplotscmd = nsosurveytools.agrisurvey:getsubplotscmd',
    ],
    },

    
    
    install_requires=["numpy", "pandas", "openpyxl", "tqdm", "natsort"],
)