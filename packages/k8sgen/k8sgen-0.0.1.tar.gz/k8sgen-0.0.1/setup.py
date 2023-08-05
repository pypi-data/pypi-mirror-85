import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

with open("k8sgen/VERSION", "r") as f:
    version = f.read()

setuptools.setup(
    name="k8sgen",
    version=version,
    author="John Carter",
    author_email="jfcarter2358@gmail.com",
    license="MIT",
    description="A Python package to enable dynamic generation of Kubernetes manifests",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jfcarter2358/k8sGen",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_data={'k8sgen': ['data/*.txt', 'data/APIResources/*.json', 'data/Components/*.json']},
    python_requires='>=3.7',
)