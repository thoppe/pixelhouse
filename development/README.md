### Release Notes:

+ `black --line-length 80 pixelhouse unincorporated_demos/ tests/`
+ Update the version number in `pixelhouse/_version.py`
+ `python setup.py sdist` Build the distribution file.
+ `twine upload -r test dist/*` Push the release to [pypi test](https://test.pypi.org/project/nlpre/) 
+ `twine upload dist/*` Push the release to [pypi live](https://pypi.org/project/nlpre/)

## Development notes

+ Before a push run `black` (`pip install black`) to keep the code tidy.
+ Tests can be run using `tox` (`pip install tox`), using nosetest (but be aware that python3.6 is needed for the tests so make sure nose is up-to-date.

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
