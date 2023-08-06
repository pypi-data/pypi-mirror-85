import setuptools

setuptools.setup(
    name="linechart_animator",
    version="0.0.6",
    author="Péntek Zsolt",
    description="Create animated plots",
    long_description='',
    long_description_content_type="text/markdown",
    url="https://github.com/Zselter07/linechart_animator",
    packages=setuptools.find_packages(),
    install_requires=["numpy", "scipy", "matplotlib"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)