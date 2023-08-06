import setuptools

# with open("README.md", "r") as fh:
#     long_description = fh.read()
long_description = "Evaluate whisper."
setuptools.setup(
    name="whisper-evaluate",
    version="1.2.25",
    author="geb",
    author_email="853934146@qq.com",
    description="Evaluate the effectiveness of the Whisper model.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://git.xindong.com/fengyanglu/whisper-evaluate",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=['numpy', 'pandas', 'aiohttp', 'tqdm', 'pandarallel', 'requests'],
    python_requires='>=3.6',
)
