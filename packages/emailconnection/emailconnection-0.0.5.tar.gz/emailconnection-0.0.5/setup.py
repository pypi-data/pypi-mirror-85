from setuptools import setup

setup(
    name='emailconnection',
    packages=['emailconnection'],
    package_dir={'emailconnection': 'src/emailconnection'},
    version='0.0.5',
    license='MIT',
    platforms='cross-platfom, platform-independent',
    description='Email Connections and Queries Handler',
    author='Yogesh Yadav',
    author_email='yogeshdtu@gmail.com',
    url='https://github.com/ByPrice/emailconnection',
    download_url='https://github.com/ByPrice/emailconnection',
    keywords=['email', 'emailconnection'],
    install_requires=[
       'python-dotenv>=0.10.3', 'python-dateutil >=2.8.1'
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'Programming Language :: Python :: 3.6',
    ],
)
