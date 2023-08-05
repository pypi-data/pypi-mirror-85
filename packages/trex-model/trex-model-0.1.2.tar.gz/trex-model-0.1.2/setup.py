import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
     name='trex-model',  
     version='0.1.2',
     author="Jack Lok",
     author_email="sglok77@gmail.com",
     description="TRex database module package",
     long_description=long_description,
     long_description_content_type="text/markdown",
     url="https://bitbucket.org/lokjac/trex-model",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
     include_package_data = True,
     install_requires=[            
          'google-cloud-firestore',
          'google-cloud-datastore',
          'google-cloud-ndb',
          'flask-login',
          'six',
          'trex-lib',
      ]
 )

