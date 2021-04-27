from setuptools import setup, find_packages

with open('README.md', 'rt', encoding='utf-8') as f:
    long_desc = f.read()

# Setup module
setup(
    # Module name
    name="discord.py-buttons",
    # Module version
    version="1.0.0",
    # License - MIT!
    license='MIT',
    # Author (Github username)
    author="Lapis0875",
    # Author`s email.
    author_email="lapis0875@kakao.com",
    # Short description
    description="Wrapper of discord buttons features for discord.py",
    # Long description in REAMDME.md
    long_description_content_type='text/markdown',
    long_description=long_desc,
    # Project url
    url="https://github.com/Lapis0875/dpy_buttons",
    # Include module directory 'embed_tools'
    packages=find_packages(),
    # Dependencies : This project depends on module 'discord.py'
    install_requires=["discord.py>=1.7.1"],
    # Module`s python requirement
    python_requires=">=3.7",
    # Keywords about the module
    keywords=["discord api", "discord.py", "discord buttons"],
    # Tags about the module
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
)