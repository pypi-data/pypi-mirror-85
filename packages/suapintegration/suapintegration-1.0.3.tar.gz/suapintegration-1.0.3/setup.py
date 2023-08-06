from setuptools import setup
# from distutils.core import setup
setup(
    name='suapintegration',
    description='Utils and theme classes for SUAP-EAD project services',
    long_description='Utils and theme classes for SUAP-EAD project services',
    license='MIT',
    author='Kelson da Costa Medeiros, Luiz Antonio Freitas de Assis',
    author_email='kelsoncm@gmail.com, luizvpc@gmail.com',
    packages=['suapintegration'],
    include_package_data=True,
    version='1.0.3',
    download_url='https://github.com/suap-ead/lib_suapintegration/releases/tag/1.0.3',
    url='https://github.com/suap-ead/lib_suapintegration',
    keywords=['SUAP', 'EAD', 'complemento', 'oAuth2', 'Django', 'Auth', 'SSO', 'client', 'Theme', ],
    install_requires=['django>=2.0.0', 'social-auth-app-django', 'sc4py>=0.1.3'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ]
)
