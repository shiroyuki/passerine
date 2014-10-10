from distutils.core import setup

setup(
    name         = 'tori',
    version      = '3.0.0',
    description  = 'Micro Web Framework and ORM for MongoDB',
    author       = 'Juti Noppornpitak',
    author_email = 'juti_n@yahoo.co.jp',
    url          = 'http://shiroyuki.com/work/projects-tori',
    packages     = [
        'demo',
        'demo.app',
        'demo.app.controller',
        'demo.app.views',
        'demo.resources',
        'tori',
        'passerine.cli',
        'passerine.data',
        'passerine.db',
        'passerine.db.driver',
        'passerine.db.metadata',
        'passerine.decorator',
        'passerine.session',
        'passerine.session.entity',
        'passerine.session.repository',
        'passerine.socket',
        'passerine.template'
    ],
    scripts          = ['bin/nest'],
    install_requires = ['imagination', 'kotoba', 'tornado', 'jinja2', 'pymongo']
)
