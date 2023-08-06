from distutils.core import setup
setup(
  name = 'TOPSIS-mansi-101803412',         # How you named your package folder (MyLib)
  packages = ['TOPSIS-mansi-101803412'],   # Chose the same as "name"
  version = '1.0.1',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Calculating Topsis Score can help in understanding best and worst data entries in a dataset.In this package ,we are calculating topsis rank by taking input csv file,weights and impacts from the user.-Weights and impacts must be comma separated -Number of Columns in the dataset should be equal to number of weights and number of impacts passed.',   #e add short description about your library
  author = 'Mansi gupta',                   # Type in your name
  author_email = 'guptamansi2712@gmail.com',      # Type in your E-Mail
  #url = 'https://github.com/guptamansi2712/TOPSIS-mansi-101803412',   # Provide either the link to your github or to your website
  #download_url = 'https://github.com/user/reponame/archive/v_01.tar.gz',    # I explain this later on
  keywords = ['Topsis', 'Vector normalization', 'Topsis score'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'pandas','numpy','scipy'
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