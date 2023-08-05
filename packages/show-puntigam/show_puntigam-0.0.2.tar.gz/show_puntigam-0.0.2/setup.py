import setuptools

with open('README.md') as readme_file:
    README = readme_file.read()

with open('HISTORY.md') as history_file:
    HISTORY = history_file.read()

install_requires = [
    'numpy',
    'pyvista'
]

setup_args = dict(name='show_puntigam',
      version='0.0.2',
      description='Python package to evaluate urban lidar datasets.',
      long_description=README,
      long_description_content_type="text/markdown",
      url="https://gitlab.v2c2.at/michaelhartmann/show_puntigam",
      download_url="https://gitlab.v2c2.at/michaelhartmann/show_puntigam",
      packages=setuptools.find_packages(),
      author_email='michael.hartmann@v2c2.at',
      zip_safe=False)
if __name__ == '__main__':
    setuptools.setup(**setup_args)
