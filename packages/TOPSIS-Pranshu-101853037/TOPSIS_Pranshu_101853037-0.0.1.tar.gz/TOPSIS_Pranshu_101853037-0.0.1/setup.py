from setuptools import setup

def readme():
    with open('README.md') as f:
        README = f.read()
    return README

setup(
    name='TOPSIS_Pranshu_101853037',
    packages=['TOPSIS_Pranshu_101853037'],
    version='0.0.1',
    license='MIT',
    description='This is a Python Package implementing TOPSIS used for multi-criteria decision analysis method',
    long_description=readme(),
    long_description_content_type='text/markdown',
    author='Pranshu Jindal',
    author_email='pranshujindal7@gmail.com',
    url='https://github.com/pranshu1229/topsispy',
    download_url = 'https://github.com/pranshu1229/topsispy/archive/v_01.tar.gz',
    keywords=['topsis', 'becoe', 'UCS538', 'TIET'],
    install_requires=[
        'numpy',
        'pandas',
    ],
    include_package_data=True,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
    ],
)