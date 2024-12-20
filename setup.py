from setuptools import setup, find_packages

setup(
    name='hdub-mud',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'python-dotenv==1.0.0',
        'pytest',
        'gunicorn',
        'quart-cors==0.1.2',
        'gino==1.0.1',
        'quart>=0.15.1',
        'quart-auth==0.6.0',
        'gino-quart==0.1.2',
        'asyncpg>=0.27.0',
        'aiofiles==0.6.0',
        'blinker==1.4',
        'hypercorn==0.14.3',
        'jinja2==2.11.3',
        'werkzeug>=2.0.0',
        'alembic==1.12.0',
        'markupsafe==2.0.1',
        'importlib_metadata==3.10.1',
        'setuptools>=57.0.0',
        'pyJWT==2.8.0',
    ],
)
