from setuptools import setup

def readme():
  with open('README.md') as f:
    return f.read()

setup(name='word_tree',
      version='1.1.1',
      description='Dictionary optimised for progressive lookup',
      long_description=readme(),
      long_description_content_type='text/markdown',
      keywords='dictionary word incremental lookup',
      url='https://gitlab.com/OldIronHorse/word_tree',
      author='Simon Redding',
      author_email='s1m0n.r3dd1ng@gmail.com',
      license='GPL3',
      packages=['word_tree'],
      test_suite='nose.collector',
      tests_require=['nose'],
      include_package_data=True,
      zip_safe=False)
