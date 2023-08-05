from setuptools import setup, find_packages
from io import open
from os import path
import pathlib
# The directory containing this file
HERE = pathlib.Path(__file__).parent
# The text of the README file
README = (HERE / "README.md").read_text()
# automatically captured required modules for install_requires in requirements.txt and as well as configure dependency links
with open(path.join(HERE, 'requirements.txt'), encoding='utf-8') as f:
    all_reqs = f.read().split('\n')
install_requires = [x.strip() for x in all_reqs if ('git+' not in x) and (
    not x.startswith('#')) and (not x.startswith('-'))]
dependency_links = [x.strip().replace('git+', '') for x in all_reqs
                    if 'git+' not in x]

setup(
    name="django-cli-g73",  # Replace with your own username
    version="0.1.1",
    author="Wilson Padilla",
    author_email="wdavidw26@gmail.com",
    description="This is a small project created with the initial purpose of facilitating, through a single command, the creation of views(views), templates(templates), models(models) and serializers(serializers) for the django web framework.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/wdavid73/django-cli",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=install_requires,
    license='MIT',
    dependency_links=dependency_links,
    entry_points='''
        [console_scripts]
        django-cli=cli.main:main
    '''
)
