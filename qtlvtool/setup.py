from setuptools import setup, find_packages

setup(
    name='qtlvtool',
    version='0.1',
    author='Alexandre Dutrieux',
    include_package_data=True,
    packages=[
        'app', 'app.models', 'app.serialization', 
        'app.views', 'app.views.core', 'app.views.elements', 
        'app.views.elements.scenes', 'app.views.graphics', 'app.views.widgets',
        'app.views.widgets.tabs', 'resource', 'resource.icons'
    ]
)