from distutils.core import setup
setup(
  name = 'TOPSIS-Anshul-101803408',         # How you named your package folder (MyLib)
  packages = ['TOPSIS-Anshul-101803408'],   # Chose the same as "name"
  version = '0.1',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'This Library helps to generate TOPSIS score as well as Rank for any given set of Model Parameters',   # Give a short description about your library
  author = 'Anshul Jain',                   # Type in your name
  author_email = 'anshulj802@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/anshuljain2607/TOPSIS-Anshul-101803408.git',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/anshuljain2607/TOPSIS-Anshul-101803408/archive/v_01.tar.gz',    # I explain this later on
  keywords = ['TOPSIS'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
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