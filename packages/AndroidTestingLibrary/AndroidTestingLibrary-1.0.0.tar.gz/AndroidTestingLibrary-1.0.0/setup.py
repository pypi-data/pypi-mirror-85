import setuptools

with open("README.md", "r") as file:
    long_description = file.read()

setuptools.setup(
    name = "AndroidTestingLibrary",
    version = "1.0.0",
    author = "Carlos Bernal, Aidan Connor, Nathan Cooper, Miodrag Dronjak, Kaitlyn Huynh, Dominic Peterson, Denys Poshyvanyk, Evelyn Showalter, Daniel White",
    author_email = "ajconnor@email.wm.edu",
    description = "Library for automated testing of Android applications",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://gitlab.com/wm-csci435-f20/android-testing-library",
    packages = setuptools.find_packages(),
    install_requires = [
        "pure-python-adb>=0.3.0.dev0",
        "nltk>=3.5"
    ],
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
