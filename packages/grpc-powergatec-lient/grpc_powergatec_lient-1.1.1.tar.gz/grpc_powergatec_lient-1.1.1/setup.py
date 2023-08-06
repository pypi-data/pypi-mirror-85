import setuptools

setuptools.setup(
    name="grpc_powergatec_lient",
    version="1.1.1",
    author="Textile",
    author_email="contact@textile.io",
    url="https://github.com/textileio/powergate",
    packages=setuptools.find_packages(where="src"),
    package_dir={'': 'src'},
    install_requires=[
      'protobuf',
      'grpcio',
    ],
)
