from setuptools import setup

def readme():
  with open('README.md') as f:
    return f.read()

setup(name='squeezebox-cli',
      version='0.1.7',
      description='A command line interface to control Squeezebox.',
      long_description=readme(),
      long_description_content_type='text/markdown',
      keywords='',
      url='http://gitlab.com/OldIronHorse/squeezebox-cli',
      author='Simon Redding',
      author_email='s1m0n.r3dd1ng@gmail.com',
      license='GPL3',
      packages=[
          'squeezebox_cli',
          'squeezebox_cli.core',
          'squeezebox_cli.player',
          'squeezebox_cli.database',
          ],
      scripts=[
          'bin/squeezebox',
          ],
      python_requires='>=3.6',
      install_requires=[
          'click',
          'tabulate',
          'dateparser',
          'pyyaml',
          ],
      test_suite='nose.collector',
      tests_require=['nose', 'nosy'],
      include_package_data=True,
      zip_safe=False)
