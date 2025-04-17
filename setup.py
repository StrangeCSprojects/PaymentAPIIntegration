from setuptools import setup, find_packages

# Package setup configuration
setup(
    # Basic metadata
    name='payment-api',
    version='0.1',

    # Automatically discover all packages/modules
    packages=find_packages(),
    include_package_data=True,

    # Dependencies required for installation
    install_requires=[
        'flask==3.0.3',
        'sqlalchemy==2.0.28',
        'Flask-SQLAlchemy==3.1.1',
        'mysql-connector-python==9.2.0',
        'PyMySQL==1.1.1',
        'cryptography==44.0.2',
        'zappa==0.59.0',
    ],

    # Define CLI entry points for executing the app
    entry_points={
        'console_scripts': [
            'run-api = process_payement:app'
        ]
    },
)
