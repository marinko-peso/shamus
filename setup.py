from setuptools import setup, find_packages


setup(
    name='shamus',
    version='0.7',
    description='Small python decorator for basic method time and memory usage.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    keywords='decorator memory time method',
    url='https://github.com/marinko-peso/shamus',
    author='Marinko Peso',
    author_email='marinko.peso@gmail.com',
    license='MIT',
    packages=find_packages(exclude=['tests*']),
    install_requires=[
        'psutil>=5.0.0',
    ],
    zip_safe=False,
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ]
)
