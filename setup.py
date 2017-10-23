from setuptools import setup, find_packages


setup(
    name='EzLogging',
    version='0.1.0',
    description='Ez Logging.',
    author='Muream',
    author_email='muream@gmail.com',
    license='MIT',
    packages=find_packages(),
    install_requires=['pyside', 'keyboard'],
    dependency_links=['https://gitlab.com/kukulkan/core-packages'],
    url='https://github.com/muream/EzLogging',
    download_url='git+https://github.com/muream/EzLogging',
)
