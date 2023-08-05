from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()


setup(
    name="openspeechcorpus",
    version="0.2.1",
    description="The CLI for perform actions over the Open Speech Corpus",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/open-speech-org/openspeechcorpus-cli",
    keyboards="speech corpus",
    author="contraslash S.A.S.",
    author_email='ma0@contraslash.com',
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    license="MIT",
    install_requires=[
        "requests>=2.22.0"
    ],
    packages=[
        "openspeechcorpus_cli",
        "openspeechcorpus_cli.cmu_sphinx",
        "openspeechcorpus_cli.htk",
        "openspeechcorpus_cli.utils",
    ],
    scripts=[
        "openspeechcorpus_cli/bin/ops",
        "openspeechcorpus_cli/bin/recursive_convert",
        "openspeechcorpus_cli/bin/configure_sphinx",
        "openspeechcorpus_cli/bin/clean_previous_configuration",
        "openspeechcorpus_cli/bin/generate_sphinx_language_model",
        "openspeechcorpus_cli/bin/configure_htk",
        "openspeechcorpus_cli/bin/generate_htk_flat_start",
    ],
    zip_safe=False,
    include_package_data=True,
    project_urls={
        "Bug Reports": "https://github.com/open-speech-org/openspeechcorpus-cli/issues",
        "Source": "https://github.com/open-speech-org/openspeechcorpus-cli",
        "Contraslash": "https://contraslash.com/"
    },
)
