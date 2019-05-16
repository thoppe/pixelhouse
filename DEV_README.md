## pypi Notes

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

### Release Notes:

+ Update the version number in `pixelhouse/_version.py`
+ Test release, check coverage, and lint
+ Push the release to [pypi live](https://pypi.org/project/pixelhouse/)

    tox
    black --line-length 80 pixelhouse unincorporated_demos/ tests/
    rm dist/ -rvf && python setup.py sdist
    twine upload -r test dist/*
    twine upload dist/*