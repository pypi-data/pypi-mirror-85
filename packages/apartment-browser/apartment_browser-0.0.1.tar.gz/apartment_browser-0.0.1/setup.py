import setuptools


def list_requirements():
    with open('requirements') as requirements_file:
        requirements = [
            row.split(';')[0]
            for row in requirements_file.read().split('\n')
            if not row.startswith('#') and not row.startswith('-i') and len(row.strip()) > 0
        ]
    return requirements


setuptools.setup(
    name='apartment_browser',
    description='Backend used by "apartment browser" web extensions',
    version='0.0.1',
    packages=setuptools.find_packages(),
    install_requires=list_requirements()
)
