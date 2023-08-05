from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 2 - Pre-Alpha',
    'Intended Audience :: Education',
    'Operating System :: MacOS :: MacOS X',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='manim_live',
    version='0.0.10',
    description='Program that uses manim and can display animations and be controlled live',
    long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='',
    author='Cory Alexander Balaton',
    author_email='cory.balaton@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='animations',
    packages=find_packages(),
    install_requires=['pyglet==1.5.8']
)