from distutils.core import setup
from setuptools import find_packages
from setuptools.command.install import install
import os

class PostInstallCmd(install):
    def run(self):
        os.system('pip install ./meshpy')
        os.system('pip install ./dexnet')
        os.system('cd graspnms\npip install .')
        install.run(self)

os.system('pip install cython numpy')

setup(
    name='graspnetAPI',
    version='1.0.0',
    description='graspnet API',
    author='Hao-Shu Fang, Chenxi Wang, Minghao Gou',
    author_email='gouminghao@gmail.com',
    url='https://graspnet.net',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'cython',
        'scipy',
        'transforms3d==0.3.1',
        'open3d>=0.8.0.0',
        'trimesh==3.8.4',
        'tqdm',
        'Pillow==7.2.0',
        'opencv-python',
        'pillow',
        'matplotlib',
        'pywavefront',
        'trimesh',
        'scikit-image',
        'autolab_core',
        'autolab-perception',
    ],
    cmdclass={
        'install': PostInstallCmd
    }
)




# setup(name='dexnet',
#     version='0.2.0',
#     description='Dex-Net project code',
#     author='Jeff Mahler',
#     author_email='jmahler@berkeley.edu',
#     package_dir = {'dexnet'},
#     packages=['dexnet']
# )


# setup(name='meshpy',
#     version='0.1.0',
#     description='MeshPy project code',
#     author='Matt Matl',
#     author_email='mmatl@berkeley.edu',
#     package_dir = {'': '.'},
#     packages=['meshpy'],
#     #ext_modules = [meshrender],
#     install_requires=requirements,
#     test_suite='test',
#     cmdclass={
#         'install': PostInstallCmd,
#         'develop': PostDevelopCmd
#     }
# )

# print('installing meshpy')
# os.system('pip install ./meshpy')

# print('installing dexnet')
# os.system('pip install ./dexnet')