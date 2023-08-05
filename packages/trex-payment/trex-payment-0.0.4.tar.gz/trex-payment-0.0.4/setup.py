import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()
    
setuptools.setup(
    #Application name and details
     name='trex-payment',
     description="TRex Payment library package",
     long_description=long_description,
     long_description_content_type="text/markdown",  
     url="https://bitbucket.org/lokjac/trex-payment",
     version='0.0.4',
     
     #Author details
     author="Jack Lok",
     author_email="sglok77@gmail.com",
     
     #packages=setuptools.find_packages(),
     packages=setuptools.find_packages(),
     
     #include additional files
     package_data = {
        # If any package contains *.txt or *.rst files, include them:
        '': ['*.*'],
     },
     
     include_package_data=True,
     
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
     install_requires=[            
          'stripe',
          'flask',
          'flask_google_cloud_logger',
          'trex-lib',
          'trex-model',
          'trex-web',
      ],
 )

