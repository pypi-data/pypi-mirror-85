from setuptools import setup


def readme():
    with open('README.md') as file:
        README = file.read()
    return README


setup(
    # How you named your package folder (MyLib)
    name='TOPSIS_Ajat_101803268',
    packages=['TOPSIS_Ajat_101803268'],   # Chose the same as "name"
    version='0.1',      # Start with a small number and increase it with every change you make
    # Chose a license from here: https://help.github.com/articles/licensing-a-repository
    license='MIT',
    # Give a short description about your library
    description='A python package for Multiple Criteria Decision Making (MCDM) using Topsis',
    long_description=readme(),
    long_description_content_type="text/markdown",
    author='Ajat Suneja',                   # Type in your name
    author_email='sunejaajat71@gmail.com',      # Type in your E-Mail
    # Provide either the link to your github or to your website
    url='https://github.com/Ajat-beep/TOPSIS_Ajat_101803268',
    # I explain this later on
    download_url='https://github.com/Ajat-beep/TOPSIS_Ajat_101803268/archive/0.1.tar.gz',
    keywords=['TOPSIS'],   # Keywords that define your package best
    install_requires=[            # I get to this in a second
        'pandas',
    ],
    classifiers=[
        # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Development Status :: 3 - Alpha',
        # Define that your audience are developers
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',   # Again, pick a license
        # Specify which pyhton versions that you want to support
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
