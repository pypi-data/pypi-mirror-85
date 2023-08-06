from setuptools import setup


def read(fname):
    import os
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(name='pad-sequences',
      version='0.5.0',
      description='pad variable length sequences with multiples features',
      long_description=read('README.md'),
      long_description_content_type='text/markdown',
      url='http://github.com/ulf1/pad-sequences-multi',
      author='Ulf Hamster',
      author_email='554c46@gmail.com',
      license='MIT',
      packages=['pad_sequences'],
      install_requires=[
          'setuptools>=40.0.0'],
      python_requires='>=3.5',
      zip_safe=False)
