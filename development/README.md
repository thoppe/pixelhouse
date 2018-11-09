## Development notes

+ Update the version number in `pixelhouse/_version.py`
+ Build the distribution file `python setup.py sdist`

Use the following `~/.pypirc` file (with an updated username and password)

    [distutils]
    index-servers=
        pypi
        test
    
    [test]
    repository=https://test.pypi.org/legacy/
    username=
    password=
    
    [pypi]
    repository = https://upload.pypi.org/legacy/
    username=
    password=

+ Push the release to [pypi test](https://test.pypi.org/project/nlpre/) `twine upload -r test dist/*`
+ Push the release to [pypi live](https://pypi.org/project/nlpre/) `twine upload dist/*`
