from setuptools import setup, find_packages
from os.path import join, dirname
import apium

setup(
    name='apium-dev',
    version=apium.__version__,
    packages=find_packages(),
    description='Python JSON-RPC Framework',
    long_description=open(join(dirname(__file__), 'README.rst')).read(),
    author='Alexandr Katsko',
    license='LGPLv3',
    url='https://apium.dev/',
)
