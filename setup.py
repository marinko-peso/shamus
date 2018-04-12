from setuptools import setup, find_packages


setup(
    name='shamus',
    version='0.4',
    description='Small python decorator for basic method time and memory usage.',
    long_description=open('README.md').read(),
    keywords='decorator memory time method',
    url='https://github.com/marinko-peso/shamus',
    author='Marinko Peso',
    author_email='marinko.peso@gmail.com',
    license='MIT',
    packages=find_packages(exclude=['tests*']),
    install_requires=[
        'psutil>=5.0.0'
    ],
    zip_safe=False
)
