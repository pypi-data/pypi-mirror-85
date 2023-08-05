import setuptools

with open('README.md', 'r') as f:
    long_description = f.read()

setuptools.setup(
    name='PaiPage',
    version='1.0.3',
    author='AivanF.',
    author_email='projects@aivanf.com',
    description='A small Python library to deal with big tables',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/AivanF/PaiPage',
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
        'Environment :: Web Environment',
        'Framework :: Django CMS',
        'License :: Freely Distributable',
    ],
)
