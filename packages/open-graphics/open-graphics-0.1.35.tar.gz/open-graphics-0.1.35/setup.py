from setuptools import setup, find_packages

requirements = [
    'oss2',
    'requests',
    'numpy',
    'pandas',
    'matplotlib',
    'opencv-python',
    'flask',
    'colour-science',
    'scikit-learn',
    'scenedetect',
    'moviepy',
    'Pillow',
    'torch',
    'torchvision',
    'joblib',
    'tensorflow',
    'tensorflow-hub',
]

__version__ = '0.1.35'

setup(
    # Metadata
    name='open-graphics',
    version=__version__,
    author='CachCheng',
    author_email='tkggpdc2007@163.com',
    url='https://github.com/CachCheng/OpenGraphics',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    description='Open Graphics Toolkit',
    license='Apache-2.0',
    packages=find_packages(exclude=('docs', 'tests', 'scripts')),
    zip_safe=True,
    include_package_data=True,
    install_requires=requirements,
)
