import subprocess
from setuptools import setup, find_packages
from setuptools.command.install import install


INSTALL_REQUIREMENTS = [
    'numpy==1.19.0rc2',
    'pandas==1.0.4',
    'scikit-learn==0.23.1',
    'matplotlib',
    'pylint',
    'doxypypy',
    'pycodestyle',
    'opencv-python',
    'nltk==3.5',
    'keras==2.3.1',
    'tensorflow==2.2.0']


class InstallCommand(install):
    """
    will call activate githooks for install mode
    """
    def run(self):
        subprocess.call("git config core.hooksPath .githooks/", shell=True)
        install.run(self)

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='ds-gear',
      packages=find_packages(include=['dsg', 'dsg.*']),
      author='Marouen Azzouz, Youssef Azzouz',
      author_email='azzouz.marouen@gmail.com, youssef.azzouz1512@gmail.com',
      keywords='machine learning recurrent convolutional neural network named entity recognition sentiment analysis deep learning topic detection',
      description="Data science gear: Python API for advanced machine learning algorithms built on top of sklearn, tensorflow and keras",
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/AI-Companion/ds-gear",
      version='0.1.10',
      zip_safe=False,
      dependency_links=['git+https://www.github.com/keras-team/keras-contrib.git#egg=keras-contrib'],
      install_requires=INSTALL_REQUIREMENTS,
      package_data={'ds-gear': ['LICENSE']},
      include_package_data=True,
      python_requires='>=3.6',
      classifiers=[
          "Programming Language :: Python :: 3.6",
          "Development Status :: 3 - Alpha",
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent",],
      cmdClass={
          'install': InstallCommand
      })
