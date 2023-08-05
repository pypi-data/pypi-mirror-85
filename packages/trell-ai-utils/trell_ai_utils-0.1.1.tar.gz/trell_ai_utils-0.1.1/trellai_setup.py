"""Setup for the chocobo package."""

import setuptools


with open('README.md') as f:
    README = f.read()

setuptools.setup(
    author="Abhay Kumar",
    author_email="abhay@trell.in",
    name='trell_ai_utils',
    description='Utility code for trell ai repos',
    version='v0.1.1',
    long_description=README,
    url='https://gitlab.com/abhay7/trell-ai-util',
    packages=setuptools.find_packages(),
    python_requires=">=3.6.9",
    install_requires=['requests','emoji==0.5.4','json-utils==0.2', 'python-dotenv==0.15.0', 'pandas_gbq',
                      'google-cloud==0.34.0', 'google-cloud-bigquery==1.23.1', 'mysql-connector==2.2.9',
                        'mysql-replication==0.22', "subprocess32==3.5.4", "psutil==5.6.7",
                      "Flask == 1.1.1", "SQLAlchemy == 1.3.12", "SQLAlchemy-JSONField==0.9.0",
                      "SQLAlchemy-Utils==0.36.8", "boto==2.49.0","boto3==1.10.50",
                      ],
    classifiers=[
        # Trove classifiers
        # (https://pypi.python.org/pypi?%3Aaction=list_classifiers)
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python :: 3.6',
        'Topic :: Scientific/Engineering :: Artificial Intelligence'

    ],
)


