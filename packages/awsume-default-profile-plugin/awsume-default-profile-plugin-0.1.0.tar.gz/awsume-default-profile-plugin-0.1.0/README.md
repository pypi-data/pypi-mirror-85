# Awsume Default Profile Plugin

_Awsume 4 only._

This is a plugin that let's you specify a different default profile to use when invoking `awsume` without a specified profile name.

## Installation

Install with pip

```sh
$ pip install awsume-default-profile-plugin
```

Note: this will only work if you have also installed `awsume` with pip; the plugin will not be included if you installed `awsume` with brew.

## Configuration

Configure this plugin to override the default profile name selected when no `profile_name` positional argument is specifed in the call to `awsume`. The plugin will use the following values:

  1. The value of the `AWSUME_DEFAULT_PROFILE` environment variable if set, or

  2. The value of the `default-profile` key in your `~/.awsume/config.yaml` if set, or

  3. The value `"default"`.

If a `profile_name` or `role_arn` argument is supplied to `awsume`, this plugin will not do anything.

## Usage

I'm using [direnv](https://direnv.net/) to set the `AWSUME_DEFAULT_PROFILE` for specific directories so I can just call `awsume` without having to specific a specific profile each time (auto-complete just feels a little too slow for me).

## Development

After making changes, test by installing the plugin locally. From the repo run:

```sh
$ pip install .
```

To publish changes:

```sh
# Don't forget to increment the version number
$ python setup.py sdist bdist_wheel
$ python -m twine upload dist/*
# Clean up build artifacts
$ git clean -xdf
```

See https://packaging.python.org/tutorials/packaging-projects/ for more detail.
