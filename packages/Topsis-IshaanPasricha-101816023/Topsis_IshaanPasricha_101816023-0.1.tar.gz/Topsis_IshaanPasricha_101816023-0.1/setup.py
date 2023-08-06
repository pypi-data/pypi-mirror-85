from distutils.core import setup
setup(
  name = 'Topsis_IshaanPasricha_101816023',         # How you named your package folder (MyLib)
  packages = ['Topsis_IshaanPasricha_101816023'],   # Chose the same as "name"
  version = '0.1',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'This library helps in implementing topsis method',   # Give a short description about your library
  author = 'Ishaan Pasricha',                   # Type in your name
  author_email = 'ipasricha_be18@thapar.edu',      # Type in your E-Mail
  url = 'https://github.com/ishaan019/TOPSIS_Ishaan_Pasricha_101816023',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/ishaan019/TOPSIS_Ishaan_Pasricha_101816023/archive/v1.0.tar.gz',    # I explain this later on
  keywords = ['SIMPLE', 'TOPSIS'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'os',
		  'sys',
		  'numpy',
		  'pandas'
  
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