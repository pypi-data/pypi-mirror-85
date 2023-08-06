from setuptools import setup, find_packages
# python setup.py sdist bdist_wheel
# twine upload dist/halo-cli-0.1.tar.gz -r pypi
setup(
    name='halo-cli',
    version='0.2.7',
    packages=find_packages(),
    data_files=['halocli/schemas/halo_schema.json'],
    include_package_data=True,
    install_requires=[
        'Click==7.1.2','PyInquirer==1.0.3','rich==5.1.2','pyfiglet==0.8post1','colorama==0.4.3','termcolor==1.1.0','six==1.15.0','clint==0.5.1',#cli
        'pip==19.0.3','jsonschema==2.6.0', # pkgs + schema
        'flex==6.14.1','swagger-py-codegen==0.4.0' # swagger
    ],
    entry_points='''
        [console_scripts]
        hlo=halocli.cli:start
    ''',
    python_requires='>=3.6',
)