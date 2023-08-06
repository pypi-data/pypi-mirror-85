import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

install_requires = ['spacy==2.3.2', 'nltk']

setuptools.setup(
    name="topicsentiment", # Replace with your own username
    version="1.0.0",
    author="Kurian Benoy",
    author_email="kurian.benoy@aot-technologies.com",
    description="Tool for find topic sentiment",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='Apachine License',
    url="https://github.com/AOT-Technologies/forms-flow-ai-dev",
    install_requires=install_requires,
    packages=setuptools.find_packages(),
    python_requires='>=3.5',
    include_package_data=True
)
