import setuptools

setuptools.setup(
    name='RedeSociaisLume',
    version="0.0.1",
    url="https://gitlab.com/agencia-lume/rede-sociais-api",
    author="Agência Lume",
    author_email="ti@agencialume.com",
    description="Pacote para conexão com apis de rede sociais",
    install_requires=[
        'requests>=2.0'
    ],
    packages=setuptools.find_packages(exclude=['tests*'])

)
