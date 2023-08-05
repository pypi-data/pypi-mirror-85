from setuptools import setup, find_packages

setup(
    name             = 'travisb-django-eav2',
    version          = __import__('eav').__version__,
    license          = 'GNU Lesser General Public License (LGPL), Version 3',
    requires         = ['python (>= 3.5)', 'django (>= 1.11.14)'],
    provides         = ['eav'],
    description      = 'Entity-Attribute-Value storage for Django. Fork of django-eav-2 by Iwo Herka [hi@iwoherka.eu]',
    url              = 'http://github.com/sree93/django-eav2',
    packages         = find_packages(),
    maintainer       = 'Srinath Menon',
    maintainer_email = 'srinath@travisbickle.tech',

    classifiers  = [
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
        'Programming Language :: Python',
        'Topic :: Database',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
