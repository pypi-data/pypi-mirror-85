# PyPi public zflow redirect

## How does it work?
Check `class PostInstallCommand`

## How to manually push a new version?
### 1. Build
```
rm -rf dist/ zflow.egg-info/
python setup.py sdist
```

### 2. Push
```
twine upload dist/*
```
