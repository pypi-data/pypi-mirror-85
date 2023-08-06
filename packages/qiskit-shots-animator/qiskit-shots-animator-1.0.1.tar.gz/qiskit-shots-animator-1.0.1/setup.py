import setuptools

def readme():
    with open('README.rst') as f:
        return f.read()
			
setuptools.setup(

    name="qiskit-shots-animator",
    version="1.0.1",
    description="Software for animating quantum computing programs",
    long_description = readme(),
    long_description_content_type = "text/markdown",
    url="https://github.com/teavuihuang/qiskit-shots-animator",
    author="Tea Vui Huang",
    author_email="tvhuang@hotmail.com",
    license="Apache 2.0",
    packages=setuptools.find_packages(),
    classifiers=[
        "Environment :: Console",
        "License :: OSI Approved :: Apache Software License",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Scientific/Engineering",
    ],
    keywords="qiskit sdk quantum animation",
    include_package_data=True,
    python_requires=">=3.6",
	install_requires=[
        'matplotlib>=3.2.2',
        'numpy>=1.18.5',
        'pillow>=7.2.0',
        'pkginfo>=1.5.0.1',        
	]	
)

