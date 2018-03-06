from setuptools import setup, find_packages


VERSION = '1.2.0.dev0'


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
        'django>=1.11.0,<2.0',
        'psu.oit.wdt.emcee>=1.0.0.rc2',
        'django-arcutils>=2.24.0',
        'django-pgcli>=0.0.2',
        'djangorestframework>=3.7.7',
        'Markdown>=2.6.11',
        'psycopg2>=2.7.4'
    ],
    extras_require={
        'dev': [
            'flake8',
            'unidecode',
            'docker-compose'
        ]
    },
)
