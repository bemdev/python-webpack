python-webpack
==============

[![Build Status](https://travis-ci.org/markfinger/python-webpack.svg?branch=master)](https://travis-ci.org/markfinger/python-webpack)

Python bindings to webpack via [webpack-build](https://github.com/markfinger/webpack-build).

Parses modules with dependencies and generates static assets representing those modules, enabling you 
to package your assets so that they can be reused on the client-side.

```python
from webpack.compiler import webpack

assets = webpack('/path/to/webpack.config.js')

assets.render()  # Render elements pointing to the assets
```


Documentation
-------------

- [Installation](#installation)
- [Usage](#usage)
- [Output paths](#output-paths)
- [Development](#development)
- [Django integration](#django-integration)
- [Settings](#settings)
- [Running the tests](#running-the-tests)


Installation
------------

```
pip install python-webpack
npm install webpack webpack-build --save
```

Start webpack-build's server with `node_modules/.bin/webpack-build`


Usage
-----

python-webpack takes paths to [config files](https://webpack.github.io/docs/configuration.html) and passes
them to a compiler. Once the compiler has built the assets, it returns an object which enables you to interact
with the results of the build process.

```python
from webpack.compiler import webpack

assets = webpack('/path/to/webpack.config.js')

# Returns a string containing <script> and <link> elements pointing 
# to the generated assets
assets.render()

# Returns a string containing <link> elements pointing to any css assets
assets.render_style_sheets()

# Returns a string containing <script> elements pointing to any js assets
assets.render_scripts()

# Returns absolute paths to the generated assets on your filesystem
assets.get_paths()

# Returns urls pointing to the generated assets
assets.get_urls()

# Returns a string matching the `library` property of your config file
assets.get_library()
```

To pass context down to the config, you specify it in the `CONTEXT` setting. You can also provide
context by using the `extra_context` argument on `webpack`.

A helper is provided for configuring your config's output path, simply leave the setting undefined
and it will be preprocessed before compilation begins.


Django integration
------------------

### Installation and configuration

The following configuration should be placed in to your settings files to enable webpack to function 
seamlessly in a Django project.

Add `'webpack'` to your `INSTALLED_APPS`

```python
INSTALLED_APPS = (
    # ...
    'webpack',
)
```

Add `'webpack.django_integration.WebpackFinder'` to your `STATICFILES_FINDERS`

```python
STATICFILES_FINDERS = (
    # ...
    'webpack.django_integration.WebpackFinder',
)
```

Configure webpack to respect your project's configuration

```python
WEBPACK = {
    'STATIC_ROOT': STATIC_ROOT,
    'STATIC_URL': STATIC_URL,
    'WATCH': DEBUG,
    'HMR': DEBUG,
    'CONTEXT': {
        'DEBUG': DEBUG,
    },
}
```


### Path resolution

When used in a Django project, Webpack allows you to specify relative paths to config files which will be 
resolved with Django's file finders.

For example, `webpack('app/webpack.config.js')` could match a file within an app's static directory, 
such as `/project/app/static/app/webpack.config.js`.


### Template tags

A template tag is provided as a shorthand for rendering assets.

```html
{% load webpack %}

{% webpack 'app/webpack.config.js' %}
```


Settings
--------

If you are using this library in a Django project, please refer to the [Django integration](#django-integration)
section of the documentation.

Settings can be defined by calling `webpack.conf.settings.configure` with keyword arguments matching 
the setting that you want to define. For example

```python
from webpack.conf import settings

DEBUG = True

settings.configure(
    STATIC_ROOT='/path/to/your/projects/static_root',
    STATIC_URL='/static/',
    WATCH=DEBUG,
    HMR=DEBUG,
    CONTEXT: {
        'DEBUG': DEBUG,
    },
)
```


### STATIC_ROOT

An absolute path to the root directory that you use for static assets.

For example, `'/path/to/your/projects/static_root'`.

This setting **must** be defined.

Default: `None`


### STATIC_URL

The root url that your static assets are served from.

For example, `'/static/'`.

This setting **must** be defined.

Default: `None`


### CONFIG_DIRS

A list of paths that will be used to resolve relative paths to config files.

Default: `None`


### WATCH

A boolean flag which indicates that file watchers should be set to watch the assets's source
files. When a change is detected, the files which have changed are recompiled in the background
so that the assets are ready for the next request.

Set this to `True` in development environments.

Default: `False`


### HMR

A boolean flag indicating that webpack-build should inject a HMR runtime into the generate bundle.
When your assets are rendered on the front-end, they open sockets to the build server and listen
for changes.

Once assets have been recompiled, they will attempt to safely update the page. If they cannot perform
the update safely, console logs will indicate that a refresh is required.

Set this to `True` in development environments.

Default: `False`


### CONTEXT

The default context provided to config functions. This sets default values for the context object,
these values can be overridden when calling `webpack`.

Default: `None`


### CACHE

A flag indicating that webpack-build should maintain a persistent file cache.

Default: `True`


### CACHE_DIR

An override for the directory that webpack-build uses to store cache files.

Default: `None`


### OUTPUT_DIR

The directory in `STATIC_ROOT` which webpack will output all assets to.

Default: `'webpack_assets'`


### AGGREGATE_TIMEOUT

The delay between the detection of a change in your source files and the start of a compiler's
rebuild process.

Default: `200`


### POLL

If defined, this is a flag which indicates that watching compilers should poll for file changes, rather
than relying on the OS for notifications.

If the compiler is not detecting changes to your files, setting this to `True` may resolve the problem.

Default: `None`


Running the tests
-----------------

```bash
pip install -r requirements.txt
npm install
python runtests.py
```
