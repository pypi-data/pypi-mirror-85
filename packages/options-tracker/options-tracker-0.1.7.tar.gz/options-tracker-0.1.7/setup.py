from setuptools import setup

def readme():
  with open('README.md') as f:
    return f.read()

setup(name='options-tracker',
      version='0.1.7',
      description='What are my options worth today?',
      long_description=readme(),
      long_description_content_type='text/markdown',
      keywords='',
      url='http://gitlab.com/OldIronHorse/options-tracker',
      author='Simon Redding',
      author_email='s1m0n.r3dd1ng@gmail.com',
      license='GPL3',
      packages=['optionstracker'],
      scripts=[
          'bin/options-tracker',
          'bin/options-file-tracker',
          ],
      python_requires='>=3.6',
      install_requires=[
          'click',
          'requests_html',
          'dateparser',
          'python-dateutil',
          'pyyaml',
          'tabulate',
          ],
      test_suite='nose.collector',
      tests_require=['nose', 'nosy'],
      include_package_data=True,
      zip_safe=False)
