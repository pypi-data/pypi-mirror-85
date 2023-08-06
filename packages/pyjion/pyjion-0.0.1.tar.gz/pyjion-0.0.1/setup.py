from skbuild import setup
from packaging.version import LegacyVersion
from skbuild.exceptions import SKBuildError
from skbuild.cmaker import get_cmake_version

# Add CMake as a build requirement if cmake is not installed or is too low a version
setup_requires = []
try:
    if LegacyVersion(get_cmake_version()) < LegacyVersion("3.2"):
        setup_requires.append('cmake')
except SKBuildError:
    setup_requires.append('cmake')


setup(
    name='pyjion',
    version='0.0.1',
    description='A JIT compiler wrapper for CPython',
    author='Anthony Shaw',
    author_email='anthonyshaw@apache.org',
    url='https://github.com/tonybaloney/Pyjion',
    license='MIT',
    packages=['pyjion'],
    setup_requires=setup_requires,
    python_requires='>=3.9',
    include_package_data=True,
    #cmake_args=['-DDUMP_TRACES=1']
)
