from setuptools import setup

setup(
    name="outline-cli",
    use_scm_version=True,
    author="Jimmy Chen",
    author_email="jimmychen260@gmail.com",
    project_urls={
        "Bug Tracker": "https://github.com/JMCFTW/outline-cli/issues",
        "Source Code": "https://github.com/JMCFTW/outline-cli/",
    },
    setup_requires=["setuptools_scm"],
    packages=["outline_cli"],
    package_dir={"": "src"},
    entry_points={"console_scripts": ["outline-cli=outline_cli:init_cli"]},
    install_requires=[
        "certifi==2020.6.20",
        "chardet==3.0.4",
        "idna==2.10",
        "requests==2.24.0",
        "requests-toolbelt==0.9.1",
        "urllib3==1.25.11",
        "PyInquirer==1.0.3",
    ],
    zip_safe=True,
    include_package_data=True,
    python_requires=">3.6",
)
