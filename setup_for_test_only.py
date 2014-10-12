from distutils.core import setup

setup(
    name         = 'passerine',
    version      = '1.0.0rc',
    author       = 'Juti Noppornpitak',
    author_email = 'juti_n@yahoo.co.jp',
    packages     = [
        'passerine',
        'passerine.db',
        'passerine.db.driver',
        'passerine.db.metadata'
    ],
    install_requires = ['pymongo']
)
