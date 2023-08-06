from distutils.core import setup
setup(
  name = 'TOPSIS_RATAN_101803156',         # How you named your package folder (MyLib)
  packages = ['TOPSIS_RATAN_101803156'],   # Chose the same as "name"
  version = '1.0',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = ' TOPSIS is an acronym that stands for ‘Technique of Order Preference Similarity to the Ideal Solution’ and is a pretty straightforward MCDA method. As the name implies, the method is based on finding an ideal and an anti-ideal solution and comparing the distance of each one of the alternatives to those. ',   # Give a short description about your library
  author = 'RATAN KUMAR',                   # Type in your name
  author_email = 'rkumar_be18@thapar.edu',      # Type in your E-Mail
  url = 'https://github.com/ratan900',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/ratan900/TOPSIS_RATAN_101803156/archive/v_1.zip',    # I explain this later on
  keywords = ['TOPSIS', 'RATAN', '101803156'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'numpy',
          'pandas',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)
