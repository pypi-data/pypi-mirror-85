# Django-Frontier

### `The django front-end scaffold tool you requested.`

django-frontier enable you to quickly scaffold a front-end for your django apps.

`currently only (react, tailwindcss and react-tailwindcss)` scaffolding is available

---

### How to guide

before you install django-frontier, please make sure you have python install and you have a working django project either with with your local python installation or a virtual environment. We recommend the latter

1. Open your terminal and install the package using pip

```bash
$ pip install django-frontier
```

2. After the installation, add the '`frontier`' app to your django settings

```python
INSTALLED_APPS = [
...
'frontier',
...
]
```

3. Now you can use the frontier command by navigating to the root of your project directory, where 'manage.py' file is and run the frontier with either preset `(react, tailwind, or react-tailwind)`
   example for react, run:

```bash
$ python manage.py frontier react
```

or

```bash
$ ./manage.py frontier react
```

This generates a resources directory with your react application scaffold.

4. You can then compile your assets by running

```bash
$ npm run dev
```

or

```bash
$ npm run watch
```

This spits out the complied assets in a static/dist directory, which you can include in your django templates as such

```python
# settings.py
STATIC_URL = '/static/'
STATICFILES_DIRS = (str(BASE_DIR.joinpath('static')),)
```

```html
{% load static %}
<html>
<head>
...
<!-- if your dist folder includes a css files -->
<link rel="stylesheet" href="{% static 'dist/app.css' %}" />
...
</head>
<body>
<!-- for your react app -->
<div id="app"></div>
<script src="{% static 'dist/index.js' %}"></script>
</body>
</html>
...
```

For production, run the build command to minify the js and css for a smaller bundle and replace `dist/` with `build/` in your templates

```bash
$ npm run watch
```

---

#### `NOTE`: You can also configure the output destination for your bundles by configuring parcel in the `package.json` file. For more info on parcel, check out [Parcel Js](https://parceljs.org)

---

5. If you need help using the frontier command, run:

```bash
$ ./manage.py frontier -h
```

### Enjoy 😇
