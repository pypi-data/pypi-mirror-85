import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
    name='mhyt',  # How you named your package folder (MyLib)
    version='2.35',  # Start with a small number and increase it with every change you make
    license='MIT',  # Chose a license from here: https://help.github.com/articles/licensing-a-repository
    description='Download files from youtube using simple code',  # Give a short description about your library
    author='matan h',  # Type in your name
    author_email='matan.honig2@gmail.com',  # Type in your E-Mail
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://pypi.org/project/mhyt",
    packages=['mhyt'],
    install_requires=["imageio_ffmpeg","a-pytube-fork-for-spotdl-users","pydub"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.0',
)
