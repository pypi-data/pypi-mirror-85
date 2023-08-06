import re

from datetime import datetime
from itertools import groupby

from git_commits import get_commits

# see http://semver.org
semver_regex = re.compile(
    r"^(?P<major>0|[1-9]\d*)\.(?P<minor>0|[1-9]\d*)\.(?P<patch>0|[1-9]\d*)"
    r"(?:-(?P<prerelease>(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)"
    r"(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?"
    r"(?:\+(?P<buildmetadata>[0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$"
)


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
            f"Version({self.ref},"
            f" {self.date},"
            f" breaking={self.breaking},"
            f" feature={self.feature},"
            f" fix={self.fix},"
            f" num_commits={len(self.commits)})"
        )


class Commit:
    def __init__(self, commit_dict):
        self.commit_dict = commit_dict

    def __getattr__(self, name):

        try:
            return self.commit_dict[name]
        except KeyError:
            if name == 'header':
                return self.title.split(': ', 1)[0]
            elif name == 'description':
                return (
                    self.title.split(': ', 1)[1] if ': ' in self.title else self.title
                )
            elif name == 'is_breaking':
                return self.header.lower().startswith('break')
            elif name == 'type':
                return self.header.lower().split(' ', 1)[1 if self.is_breaking else 0]
            elif name == 'scope':
                return self.header.split('(')[1][:-1] if '(' in self.header else None
            elif name == 'is_feature':
                return "feat" in self.header.lower()
            elif name == 'is_fix':
                return "fix" in self.header.lower()
            else:
                raise AttributeError(f"Attribute '{name}' not found in class Commit")

    def __repr__(self):
        return f"{self.hash[:8]} {self.title})"


def sentence(string):
    try:
        return string[0].upper() + string[1:]
    except IndexError:
        # zero-length string
        return string


def retrieve_current_version(versions, prefix=''):
    global semver_regex

    last_version = None

    for version in versions:
        if version.ref != 'HEAD':
            last_version = version.ref
            break

    if last_version is None:
        return f"{prefix}0.1.0"
    else:
        result = semver_regex.match(last_version[len(prefix) :])
        major, minor, patch = (
            int(result.group('major')),
            int(result.group('minor')),
            int(result.group('patch')),
        )

        # print(major, minor, patch)

        this_version = versions[0]

        if major == 0:
            # this is a development release and only receives minor and patch increments
            if this_version.breaking > 0:
                return f"{prefix}{major}.{minor+1}.0"
            elif this_version.feature > 0 or this_version.fix > 0:
                return f"{prefix}{major}.{minor}.{patch+1}"
            else:
                # no api changes
                return f"{prefix}{major}.{minor}.{patch}"

        else:
            # this is production release and receives major, minor, and patch increments
            if this_version.breaking > 0:
                return f"{prefix}{major+1}.0.0"
            elif this_version.feature > 0:
                return f"{prefix}{major}.{minor+1}.0"
            elif this_version.fix > 0:
                return f"{prefix}{major}.{minor}.{patch+1}"
            else:
                # no api changes
                return f"{prefix}{major}.{minor}.{patch}"


def filter_commits(commits, start=None, end=None):
    """
    Returns commits from start (exclusive) to end (inclusive).
    start must occur before end
    start and end can be a tag, or hash
    """
    if start is not None:
        for idx, c in enumerate(commits):
            if start in c['tags'] or c['hash'].startswith(start):
                commits = commits[:idx]
                break

    if end is not None:
        for idx, c in enumerate(commits):
            if end in c['tags'] or c['hash'].startswith(end):
                commits = commits[idx:]
                break

    return commits


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


def format_log(versions):

    headings = {
        'docs': "Docs",
        'feat': "Features",
        'fix': "Fixes",
        'perf': "Performance",
        'refactor': "Refactorings",
    }

    output = "# Changelog\n\n"

    for version in versions:
        output += f"\n## {version.ref} ({version.date.isoformat()[:10]})\n\n"

        for key, group in groupby(
            sorted(version.commits, key=lambda x: x.type), lambda x: x.type
        ):
            if key in headings:
                output += f"### {headings[key]}\n\n"

                for commit in sorted(group, key=lambda x: f"{x.scope} {x.description}"):
                    scope = f"{commit.scope} - " if commit.scope else ''
                    desc = commit.description
                    desc = sentence(desc) if len(scope) == 0 else desc
                    breaking = " [BREAKING]" if commit.is_breaking else ''
                    output += f"* {sentence(scope)}{desc}{breaking}\n"

                # add following newline
                output += "\n"

    return output


def write_log(log, filename):
    with open(filename, 'w') as f:
        f.write(log)


def main():
    start = 'v0.4.0'
    end = None
    commits = get_commits()
    commits_filtered = filter_commits(commits, start, end)
    versions = compile_log(commits_filtered)

    versions[0].ref = retrieve_current_version(compile_log(commits), prefix='v')
    # print(versions[0].ref)

    log = format_log(versions)
    write_log(log, "CHANGELOG.md")


if __name__ == '__main__':
    main()
