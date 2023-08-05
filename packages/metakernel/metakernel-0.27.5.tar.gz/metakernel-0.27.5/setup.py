import io
import sys

from setuptools import find_packages, setup

PY2 = (sys.version_info[0] == 2)

with io.open('metakernel/__init__.py', encoding='utf-8') as fid:
    for line in fid:
        if line.startswith('__version__'):
            version = line.strip().split()[-1][1:-1]
            break

if PY2:
    ipykernel_requires = "ipykernel (< 6.0)"
    ipykernel_install_requires = "ipykernel<6.0"
else:
    ipykernel_requires = "ipykernel"
    ipykernel_install_requires = "ipykernel"

setup(name='metakernel',
      version=version,
      description='Metakernel for Jupyter',
      long_description=open('README.rst', 'rb').read().decode('utf-8'),
      long_description_content_type='text/x-rst',
      author='Steven Silvester',
      author_email='steven.silvester@ieee.org',
      url='https://github.com/Calysto/metakernel',
      requires=[ipykernel_requires, 'pexpect (>= 4.2)'],
      install_requires=[ipykernel_install_requires, 'pexpect>=4.2'],
      extras_require={
          'activity': ['portalocker'],  # activity magic
          'parallel': ['ipyparallel'],  # parallel magic
          'test': ['pytest', 'pytest-cov', 'requests']
      },
      packages=find_packages(include=['metakernel', 'metakernel.*']),
      package_data={'metakernel': ['images/*.png']},
      python_requires='>=3.5',
      classifiers=[
          'Framework :: IPython',
          'License :: OSI Approved :: BSD License',
          'Programming Language :: Python :: 3',
          'Topic :: System :: Shells',
      ]
      )
