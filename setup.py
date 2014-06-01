from setuptools import setup

setup(
    name='TSUCMS',
    version='1.0.0',
    packages=['admin', 'admin.session', 'admin.controllers', 'config', 'models', 'controllers'],
    url='www.tsucms.com',
    license='MIT',
    author='shalva jashiashvili',
    author_email='sh.jashiashvili@gmail.com',
    description='simple cms',
    install_requires=[
        'bottle',
        'pymongo >= 2.7.1',
        'mongoengine',
        'beaker',
        'jinja2'
    ]
)
