from distutils.core import setup

setup(
    name         = 'tori',
    version      = '3.0.0a2',
    description  = 'A collection of libraries, a micro web framework based on Tornado framework, and the ORM for MongoDB',
    license      = 'MIT',
    author       = 'Juti Noppornpitak',
    author_email = 'juti_n@yahoo.co.jp',
    url          = 'http://shiroyuki.com/projects/passerine.html',
    packages     = [
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
    classifiers   = [
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries'
    ],
    scripts          = ['bin/nest'],
    install_requires = ['imagination', 'kotoba', 'tornado', 'jinja2', 'pymongo']
)
