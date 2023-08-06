from pip._vendor import pkg_resources


def get_version(package):
    package = package.lower()
    return next(
        (
            p.version
            for p in pkg_resources.working_set  # noqa: F821
            if p.project_name.lower() == package
        ),
        "No match",
    )


__version__ = get_version('whathappened')

del get_version
del pkg_resources
