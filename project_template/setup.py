from setuptools import setup, find_packages

setup(
    name="package_name",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        # "numpy",
        # "opencv-python"
    ],
)
