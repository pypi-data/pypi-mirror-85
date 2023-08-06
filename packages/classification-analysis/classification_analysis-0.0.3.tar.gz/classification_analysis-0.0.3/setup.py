import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="classification_analysis",
    version="0.0.3",
    author="sammer sallam",
    author_email="samersallam92@gmail.com",
    description="This library is to monitor your model during the training process and track the metrics to find the best model",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Samer92/classification_analysis",
    packages=["classification_analysis"],
    install_requires=['cycler==0.10.0', 'imbalanced-learn==0.7.0', 'imblearn==0.0', 'joblib==0.17.0',
                     'kiwisolver==1.2.0', 'matplotlib==3.2.2', 'numpy==1.19.0', 'pandas==1.0.5', 
                     'Pillow==7.1.2', 'pyparsing==2.4.7', 'python-dateutil==2.8.1', 'pytz==2020.1', 
                     'scikit-learn==0.23.2', 'scipy==1.5.0', 'six==1.15.0', 'threadpoolctl==2.1.0'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)