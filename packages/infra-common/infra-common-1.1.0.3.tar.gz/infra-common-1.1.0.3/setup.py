import setuptools

setuptools.setup(
    name="infra-common",
    version="1.1.0.3",
    author="Deep Instinct",
    author_email="qa@deepinstinct.com",
    description="common libraries for automation framework",
    long_description_content_type="text/markdown",
    package_dir={'common.logger': 'logger', 'common.utils': 'utils', 'common.polling': 'polling'},
    packages=['common.logger', 'common.utils', 'common.polling'],
    package_data={'': ['*.yml']},
    include_package_data=True,
    install_requires=['pyYAML'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
