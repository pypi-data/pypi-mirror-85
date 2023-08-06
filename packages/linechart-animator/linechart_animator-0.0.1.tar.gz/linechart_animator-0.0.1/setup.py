import setuptools

setuptools.setup(
    name="linechart_animator",
    version="0.0.1",
    author="Péntek Zsolt",
    description="Animate linecharts easily",
    long_description='',
    long_description_content_type="text/markdown",
    url="https://github.com/Zselter07/linechart_animator",
    packages=setuptools.find_packages(),
    install_requires=["scipy", "matplotlib", "numpy"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)