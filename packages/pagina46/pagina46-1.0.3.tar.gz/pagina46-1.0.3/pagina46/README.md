creazione pacchetto
```
python setup.py sdist
```

pubblicazione pacchetto su test
```
twine upload --verbose --repository-url https://test.pypi.org/legacy/ dist/pagina46-1.0.7.tar.gz
```

pubblicazione pacchetto su prod
```
twine upload --verbose dist/*
```

installare l'app
```
INSTALLED_APPS = [
    ...
    'pagina46'
    ...
]
```

settings:
aggiungere il context processor
```
TEMPLATES = [{
    # whatever comes before
    'OPTIONS': {
        'context_processors': [
            # whatever comes before
            "pagina46.context_processors.supporto_telefonico",
            "pagina46.context_processors.show_git_info",
        ],
    }
}]
```

nel base aggiungere
```
{% load p46static %}
{% p46_css %}
```