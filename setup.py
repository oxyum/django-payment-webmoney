
from setuptools import setup

setup(
    name='django-payment-webmoney',
    version=__import__('webmoney').__version__,
    description='WebMoney Merchant Interface support for Django.',
    author='Ivan Fedorov',
    author_email='oxyum@oxyum.ru',
    url='http://code.google.com/p/django-payment-webmoney/',
    packages=['webmoney',],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ],
    include_package_data=True,
    zip_safe=False,
)
