import setuptools

setuptools.setup(
    name="scene_cutter",
    version="0.0.3",
    author="Péntek Zsolt",
    description="ffmpeg scene cutter",
    long_description='',
    long_description_content_type="text/markdown",
    url="https://github.com/Zselter07/ffmpeg_scene_cutter",
    packages=setuptools.find_packages(),
    install_requires=["kcu"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)