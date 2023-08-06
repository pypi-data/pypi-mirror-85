import setuptools

setuptools.setup(
    name="scene_cutter",
    version="0.0.7",
    author="Péntek Zsolt",
    description="Trim scenes from a video - based on ffmpeg",
    long_description='',
    long_description_content_type="text/markdown",
    url="https://github.com/Zselter07/scene_cutter",
    packages=setuptools.find_packages(),
    install_requires=["kcu"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)