from glob import glob

from setuptools import find_packages, setup

with open("requirements.txt") as f:
    install_reqs = f.read().strip().split("\n")

reqs = [str(ir) for ir in install_reqs if not ir.startswith("#")]

with open("README.md", "r") as fh:
    long_description = fh.read()

current_version = '0.5.3.6'

with open("src/warden/static/config/version.txt", "w") as text_file:
    print(f"{current_version}", file=text_file)

add_reqs = [
    'flask', 'flask_apscheduler', 'pandas'
]

setup(
    name="alphazeta.warden",
    version=current_version,
    author="Alpha Zeta",
    author_email="alphaazeta@protonmail.com",
    description="Private Portfolio Tool - Specter Server Edition",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pxsocs/specter_warden",
    packages=find_packages("src"),
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=reqs.append(add_reqs),
    setup_requires=reqs.append(add_reqs),
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Framework :: Flask",
    ],
    python_requires=">=3.6",
)
