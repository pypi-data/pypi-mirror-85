from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.8'
]


setup(
    name='okta_python',
    version='0.1.0',
    description='Collection of Okta Modules for Okta Api',
    long_description=open('README.md').read() + '\n\n' +
    open('CHANGELOG.txt').read(),
    url='',
    author='Sunny Shahi',
    author_email='shahisunny.990@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='Okta, api',
    packages=find_packages(),
    install_requires=['requests']
)
