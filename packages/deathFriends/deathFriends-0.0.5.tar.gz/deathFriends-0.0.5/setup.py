import setuptools

with open("README.md", "r") as fh:
    readme = fh.read()

setuptools.setup(
    name='deathFriends',
    version='0.0.5',
    url='https://github.com/albertosilv/deathFriends',
    license='MIT License',
    author='José Alberto',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='jose.alberto.silva@ccc.ufcg.edu.br',
    keywords=[
        'game',
        'jogo',
        'multiplayer',
        'ação',
        'tiro',
        'online'
    ],
    description=u'Jogo de tiro multiplayer',
    packages=setuptools.find_packages(),
    install_requires=['pygame>=2.0'],
    entry_points={
        'console_scripts': ['deathFriends = deathFriends.__main__:loop']
    },
    python_requires='>=3.6',
    include_package_data=True,
)
