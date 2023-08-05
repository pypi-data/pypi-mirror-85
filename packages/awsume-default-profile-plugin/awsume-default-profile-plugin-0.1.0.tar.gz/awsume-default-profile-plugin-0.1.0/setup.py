from setuptools import setup

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="awsume-default-profile-plugin",
    version="0.1.0",
    license="MIT",
    description="This is a plugin for awsume that allows you to configure the default profile.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    entry_points={"awsume": ["default_profile = default_profile"]},
    author="Robert DiMartino",
    author_email="robert@dimartino.dev",
    url="https://github.com/rdimartino/awsume-default-profile-plugin",
    py_modules=["default_profile"],
)
