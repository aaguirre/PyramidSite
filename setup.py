import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.txt')) as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.txt')) as f:
    CHANGES = f.read()

requires = [
    'pyramid',
    'pyramid_debugtoolbar',
    'pyramid_tm',
    'SQLAlchemy',
    'transaction',
    'zope.sqlalchemy',
    'waitress',
    'pyramid_jinja2',
    'wtforms',
    'gevent',
    'pymysql',
    'pyramid_mailer',
    'gunicorn',
    'pyramid_beaker',
    ]

setup(name='PyramidSite',
      version='1.0',
      description='PyramidSite',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='Alvaro Aguirre',
      author_email='alvaro.aguirre.o@gmail.com',
      url='',
      keywords='web wsgi bfg pylons pyramid',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite='pyramidsite',
      install_requires=requires,
      entry_points="""\
      [paste.app_factory]
      main = pyramidsite:main
      [console_scripts]
      initialize_PyramidSite_db = pyramidsite.scripts.initializedb:main
      """,
      )
