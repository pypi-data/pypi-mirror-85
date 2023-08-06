from setuptools import setup
with open("readme.txt", 'r') as f:
    long_description = f.read()
setup(
   name='topsis_sarpreet_101803165',
   version='1.0.1',
   description='TOPSIS MODULE',
   license="MIT",
   long_description=long_description,
   long_description_content_type="text/markdown",
   author='sarpreet',
   author_email='tiwanasarpreet07@gmail.com',
   packages=['topsis_sarpreet_101803165'],  #same as name
   install_requires=[], #external packages as dependencies
   include_package_data=True,

   
)