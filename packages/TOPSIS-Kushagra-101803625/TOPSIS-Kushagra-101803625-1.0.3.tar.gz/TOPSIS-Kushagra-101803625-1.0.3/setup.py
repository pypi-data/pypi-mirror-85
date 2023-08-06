import pathlib
from setuptools import setup
HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setup(
  name = 'TOPSIS-Kushagra-101803625',         # How you named your package folder (MyLib)
  packages = ['TOPSIS-Kushagra-101803625'],   # Chose the same as "name"
  version = '1.0.3',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'TOPSIS method for multiple-criteria decision making (MCDM).',
  long_description = README,
  long_description_content_type = "text/markdown",   # Give a short description about your library
  author = 'Kushagra Goel',                   # Type in your name
  author_email = 'kushgoel1608@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/KushagraGoel/TOPSIS-Kushagra-101803625',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/KushagraGoel/TOPSIS-Kushagra-101803625/archive/1.0.3.tar.gz',    # I explain this later on
  keywords = ['TOPSIS'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'pandas',
          'numpy',          
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3.6',                                   #Specify which python versions that you want to support
    'Programming Language :: Python :: 3.7',    
  ],
)

