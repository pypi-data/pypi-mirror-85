import setuptools as s
f=open("readme.txt","r")
ld=f.read()
f.close()
s.setup(
    name = "WinTimer",
    version="1.1.1.1",
    author = "Piyush",
    author_email="somanip409@gmail.com",
    description="Timer",
    url="https://github.com/PS218909/",
    license="MIT",
    long_description=ld,
    long_description_content_type='text/markdown',
    packages=s.find_packages(),
    python_requires=">=3.6"
    )

                
