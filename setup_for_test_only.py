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
        'grosbeak.cli',
        'grosbeak.data',
        'grosbeak.db',
        'grosbeak.db.driver',
        'grosbeak.db.metadata',
        'grosbeak.decorator',
        'grosbeak.session',
        'grosbeak.session.entity',
        'grosbeak.session.repository',
        'grosbeak.socket',
        'grosbeak.template'
    ],
    scripts          = ['bin/nest'],
    install_requires = ['imagination', 'kotoba', 'tornado', 'jinja2', 'pymongo']
)
