import setuptools

from oomnitza_events import version


requirements = [
    'analytics-python',
    'arrow',
    'Cerberus',
    'psycopg2-binary',
]

dev_requirements = [
    'pytest',
    'pytest-pep8',
    'pytest-cov',
    'wheel',
]

setuptools.setup(
    name='oomnitza-events',
    version=version.__version__,
    packages=setuptools.find_packages(exclude=['tests']),
    description='This project is developed for tracking Oomnitza activities.',
    author='Oomnitza',
    author_email='etl-admin@oomnitza.com',
    install_requires=requirements,
    extras_require={
        'dev': dev_requirements,
    },
)