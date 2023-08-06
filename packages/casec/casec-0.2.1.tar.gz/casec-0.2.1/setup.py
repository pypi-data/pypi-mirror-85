from setuptools import setup, find_packages

with open('readme.md', 'r') as f:
    long_description = f.read()

setup(
    name='casec',
    version='0.2.1',
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'casec = casec.main:main'
        ]
    },
    url='',
    license='',
    author='Allie Fitter',
    author_email='afitter@cellcontrol.com',
    description='CLI that converts the case of strings.',
    long_description=long_description,
    long_description_content_type='text/markdown'
)
