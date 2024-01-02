from setuptools import setup, find_packages

setup(
    name='postgres_stat_profiler',
    version='0.1.0',
    url='https://github.com/rombachuk/postgres_stat_profiler',
    entry_points={
      'console_scripts' : [
          'pg_stat_profiler=postgres_stat_profiler.app:main'
      ]
    },
    packages=find_packages()
)