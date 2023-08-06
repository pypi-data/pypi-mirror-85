import re

from datetime import datetime
from itertools import groupby

# imported to make this module the base module for all external calls to functions
try:
    from whathappened.git_commits import get_commits  # noqa
except ImportError:  # for development use
    from git_commits import get_commits  # noqa

# https://semver.org/spec/v2.0.0.html
semver_regex = re.compile(
    r"^(?P<major>0|[1-9]\d*)\.(?P<minor>0|[1-9]\d*)\.(?P<patch>0|[1-9]\d*)"
    r"(?:-(?P<prerelease>(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)"
    r"(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?"
    r"(?:\+(?P<buildmetadata>[0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$"
)


class VersionFormatException(Exception):
    '''Raise when a version string can not be correctly parsed'''

    pass


class Version:
    def __init__(self, ref, date):
        self.ref = ref
        self.date = (
            datetime.strptime(date, "%a %b %d %H:%M:%S %Y %z")
            if isinstance(date, str)
            else date
        )  # str input format Wed Apr 22 18:58:54 2020 +0200

        self.breaking = 0
        self.feature = 0
        self.fix = 0

        self.commits = []

    def __repr__(self):
        return (
            f"Version('{self.ref}',"
            f" {self.date},"
            f" breaking={self.breaking},"
            f" feature={self.feature},"
            f" fix={self.fix},"
            f" num_commits={len(self.commits)})"
        )  # pragma: no cover


class Commit:

    commit_regex = re.compile(
        r"(?:(?P<breaking>break(?:ing)?)? ?(?P<type>\w+){1}"
        r" ?(?:\((?P<scope>[^\(\):]+)\))?: (?P<description>.+)|"
        r"(?P<description_alt>.+))",
        flags=re.IGNORECASE,
    )

    def __init__(self, commit_dict):
        self.commit_dict = commit_dict

    def __getattr__(self, name):

        try:
            return self.commit_dict[name]
        except KeyError:

            result = Commit.commit_regex.match(self.title)
            breaking, commit_type, scope, description, description_alt = (
                result.group('breaking'),
                result.group('type'),
                result.group('scope'),
                result.group('description'),
                result.group('description_alt'),
            )

            if name == 'description':
                return description if description is not None else description_alt
            elif name == 'is_breaking':
                return breaking is not None
            elif name == 'type':
                # group equivalent commit types
                types = {
                    'doc': 'docs',
                    'docs': 'docs',
                    'feat': 'feat',
                    'feature': 'feat',
                    'features': 'feat',
                    'fix': 'fix',
                    'fixes': 'fix',
                    'perf': 'perf',
                    'performance': 'perf',
                    'refac': 'refactor',
                    'refactor': 'refactor',
                }
                try:
                    return types[commit_type]
                except KeyError:
                    return commit_type if commit_type is not None else 'other'
            elif name == 'scope':
                return scope
            elif name == 'is_feature':
                return "feat" in self.type.lower()
            elif name == 'is_fix':
                return "fix" in self.type.lower()
            else:
                raise AttributeError(f"Attribute '{name}' not found in class Commit")

    def __repr__(self):
        return (
            f"Commit({{"
            f"'hash': '{self.hash[:6]}', "
            f"'title': '{self.title}', "
            f"}})"
        )  # pragma: no cover


def sentence(string):
    try:
        return string[0].upper() + string[1:]
    except IndexError:
        # zero-length string
        return string


def calculate_next(versions, prefix=""):
    global semver_regex

    try:
        previous = versions[1]
    except IndexError:
        # if no previous version has been found
        return f"{prefix}0.1.0"

    previous_version = previous.ref[len(prefix) :]
    result = semver_regex.match(previous_version)

    # extract version numbers if possible:
    try:
        major, minor, patch = (
            int(result.group('major')),
            int(result.group('minor')),
            int(result.group('patch')),
        )
    except AttributeError:
        raise VersionFormatException(
            f"The version number of '{previous_version}' with prefix='{prefix}' cannot"
            f" be parsed. Please enter the appropriate prefix or use a version string"
            f" like 'X.Y.Z'. See https://semver.org/spec/v2.0.0.html for more details."
        )

    latest_version = versions[0]

    if major == 0:
        # this is a development release and only receives minor and patch increments
        if latest_version.breaking > 0:
            return f"{prefix}{major}.{minor+1}.0"
        elif latest_version.feature > 0 or latest_version.fix > 0:
            return f"{prefix}{major}.{minor}.{patch+1}"
        else:
            # no api changes
            return f"{prefix}{major}.{minor}.{patch}"

    else:
        # this is production release and receives major, minor, and patch increments
        if latest_version.breaking > 0:
            return f"{prefix}{major+1}.0.0"
        elif latest_version.feature > 0:
            return f"{prefix}{major}.{minor+1}.0"
        elif latest_version.fix > 0:
            return f"{prefix}{major}.{minor}.{patch+1}"
        else:
            # no api changes
            return f"{prefix}{major}.{minor}.{patch}"


def compile_log(commits):
    """
    """

    versions = []

    # iterate through commits from latest to earliest

    # group by version
    for commit in commits:
        # make a new version if required
        if len(commit['tags']) > 0 or len(versions) == 0:
            tag = commit['tags'][0] if len(commit['tags']) > 0 else 'HEAD'
            versions.append(Version(ref=tag, date=commit['date'],))

        this_commit = Commit(commit)

        # append to current version
        versions[-1].commits.append(this_commit)

        # check if commit is breaking, feature, or fix
        if this_commit.is_breaking:
            versions[-1].breaking += 1

        if this_commit.is_feature:
            versions[-1].feature += 1

        if this_commit.is_fix:
            versions[-1].fix += 1

    # for version in versions:
    #     print(version)

    return versions


def update_latest_version(versions, prefix=""):
    '''update the HEAD reference to show the next semver version'''
    latest_version = versions[0]
    latest_version.ref = calculate_next(versions, prefix=prefix)

    return versions


def format_log(versions, emoji=False):
    output = "# Changelog"

    headings = {
        'docs': "Docs",
        'feat': "Features",
        'fix': "Fixes",
        'perf': "Performance",
        'refactor': "Refactorings",
        'other': "Other",
    }

    for version in versions:
        output += f"\n\n## {version.ref} ({version.date.isoformat()[:10]})\n"

        for key, group in groupby(
            sorted(version.commits, key=lambda x: x.type[:4]), lambda x: x.type
        ):
            if key in headings:
                if emoji:
                    raise NotImplementedError

                output += f"\n### {headings[key]}\n\n"

                for commit in sorted(group, key=lambda x: f"{x.scope} {x.description}"):
                    scope = f"{commit.scope} - " if commit.scope else ''
                    desc = commit.description
                    desc = sentence(desc) if len(scope) == 0 else desc
                    breaking = " [BREAKING]" if commit.is_breaking else ''
                    output += f"* {sentence(scope)}{desc}{breaking}\n"

    return output


def write_log(log, filename):
    with open(filename, 'w') as f:
        f.write(log)
