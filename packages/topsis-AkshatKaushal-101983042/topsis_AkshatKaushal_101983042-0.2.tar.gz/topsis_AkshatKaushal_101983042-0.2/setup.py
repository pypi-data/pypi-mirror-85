from distutils.core import setup
setup(
  name = 'topsis_AkshatKaushal_101983042',         # How you named your package folder (MyLib)
  packages = ['topsis_AkshatKaushal_101983042'],   # Chose the same as "name"
  version = '0.2',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Technique for Order of Preference by Similarity to Ideal Solution (TOPSIS).TOPSIS is based on the concept that the chosen alternative should have the shortest geometric distance from the positive ideal solution (PIS)[4] and the longest geometric distance from the negative ideal solution (NIS).',   # Give a short description about your library
  author = 'Akshat Kaushal',                   # Type in your name
  author_email = 'akshatkaush@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/akshatkaush/topsis-Akshat-101983042.git',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/akshatkaush/topsis-Akshat-101983042/archive/V_0.2.tar.gz',    # I explain this later on
  keywords = ['Topsis', 'THAPAR', 'ACTIVITY SELECTION'],   # Keywords that define your package best
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