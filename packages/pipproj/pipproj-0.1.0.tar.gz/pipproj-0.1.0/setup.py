from setuptools import setup, find_packages

with open("README.md", "r") as read_me:
    longDesc = read_me.read()

setup(
    name="pipproj",
    packages=find_packages(),
    version="0.1.0",
    license="AGPL 3.0",
    description="CLI utility to help you manage you python project like npm",
    long_description=longDesc,
    long_description_content_type="text/markdown",
    include_package_data=True,
    author="Yogesh Aggarwal",
    author_email="yogeshdev@gmail.com",
    url="https://github.com/yogesh-aggarwal/pipproj",
    download_url=
    "https://raw.githubusercontent.com/yogesh-aggarwal/pipproj/master/dist/pipproj-0.1.0.tar.gz",
    keywords=["CLI", "Environment", "Management"],
    install_requires=["pyyaml"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",  # "3 - Alpha", "4 - Beta" or "5 - Production/Stable"
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)
