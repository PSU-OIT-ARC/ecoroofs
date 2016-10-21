from setuptools import setup, find_packages


VERSION = '1.0.0.dev0'


setup(
    name='psu.oit.wdt.ecoroofs',
    version=VERSION,
    description='EcoRoofs',
    author='PSU - OIT - WDT',
    author_email='webteam@pdx.edu',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'django>=1.10.2',
        'django-arcutils>=2.13.0',
        'django-local-settings>=1.0b2',
        'django-pgcli>=0.0.2',
        'djangorestframework>=3.4.7',
        'Markdown>=2.6.7',
        'psycopg2>=2.6.2',
        'psu.oit.arc.tasks',
    ],
    extras_require={
        'dev': [
            'flake8',
            'unidecode',
        ]
    },
)
