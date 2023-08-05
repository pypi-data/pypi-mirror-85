# django-kapnoc

personnal django helpers, common across my websites


## building package

```
virtualenv env
./env/bin/pip install -r requirements.txt
./env/bin/python setup.py sdist
./env/bin/python -m twine upload --repository pypi dist/*
```


