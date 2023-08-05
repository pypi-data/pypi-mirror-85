from setuptools import find_packages, setup

setup(
    name='python-apm',
    version='1.0.8',
    author="Wesly Allan",
    license='MIT',
    author_email="weslyg22@gmail.com",
    description="Ansible Package Manager",
    url="https://github.com/WeslyG/apm",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'click',
        'pyyaml'
    ],
    keywords=['Ansible', 'Package', 'APM'],
    classifiers=[
        "Programming Language :: Python :: Implementation",
        "Programming Language :: Python :: 3",
        "Natural Language :: English",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points='''
        [console_scripts]
        apm=apm.main:cli
    ''',
)
