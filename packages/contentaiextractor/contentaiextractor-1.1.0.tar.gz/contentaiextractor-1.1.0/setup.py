from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='contentaiextractor',
      version='1.1.0',
      description='makes it easier to implement a ContentAI extractor',
      long_description=long_description,
      long_description_content_type="text/markdown",
      keywords='contentai extractor computervision cv ai ml',
      url='http://github.com/turnercode/contentai-extractor-runtime-python',
      author='John Ritsema',
      author_email='john.ritsema@turner.com',
      license='apache-2',
      packages=['contentaiextractor'],
      include_package_data=True,
      zip_safe=False)
