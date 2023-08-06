from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.8'
]


setup(
    name='testlib1',
    version='0.1.0',
    description='This is a test module, will be updating the okta module soon',
    long_description=open('README.txt').read() + '\n\n' +
    open('CHANGELOG.txt').read(),
    url='',
    author='Sunny Shahi',
    author_email='shahisunny.990@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='Okta, api',
    packages=find_packages(),
    install_requires=['']
)
