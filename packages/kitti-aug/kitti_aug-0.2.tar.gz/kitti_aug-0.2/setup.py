from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()
 
setup(name='kitti_aug',
      version='0.2',
      url='https://github.com/MariamMohamedFawzy/KittiAug',
      license='MIT',
      author='Mariam Mohamed',
      author_email='maryammohamed61@gmail.com',
      # description='Augmentation of the KITTI Dataset in BEV',
      packages=find_packages(exclude=['tests']),
      long_description=long_description,
      long_description_content_type="text/markdown",
      zip_safe=False)