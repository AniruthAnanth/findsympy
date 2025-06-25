from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="findsym",
    version="0.1.0",
    author="Aniruth Ananthanarayanan",
    author_email="aniruthananthanarayanan@my.unt.edu",
    description="FINDSYM: Symmetry detection for crystal structures",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AniruthAnanth/findsympy",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Chemistry",
        "Topic :: Scientific/Engineering :: Physics",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "visualization": ["matplotlib"],
    },
    entry_points={
        "console_scripts": [
            "findsym=findsym:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
