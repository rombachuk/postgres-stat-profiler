from setuptools import setup, find_packages

setup(
    name='postgres_stat_profiler',
    author='Andrew Rombach',
    author_email='andrew.rombachuk@gmail.com',
    version='0.1.0',
    install_requires=[
        'flask>=3.0.0',
        'flask_apscheduler>=1.13.1',
        'cryptography>=41.0.7',
        'psycopg[binary]>=3.1.16'
    ],
    url='https://github.com/rombachuk/postgres_stat_profiler',
    entry_points={
      'console_scripts' : [
          'pg_stat_profiler=postgres_stat_profiler.wsgi:main'
      ]
    },
    packages=find_packages()
)