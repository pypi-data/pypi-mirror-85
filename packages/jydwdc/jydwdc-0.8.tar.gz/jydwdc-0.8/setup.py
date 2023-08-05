from setuptools import setup, find_packages

setup(
    name="jydwdc",
    version="0.8",
    keywords="jydwdc",
    description="this is a demo",
    license="MIT License",
    author="jiangyd",
    author_email="962584902@qq.com",
    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=[],
    entry_points={
        "console_scripts": [
            "wd=jydwdc.wdc:main"
        ]
    }
)
