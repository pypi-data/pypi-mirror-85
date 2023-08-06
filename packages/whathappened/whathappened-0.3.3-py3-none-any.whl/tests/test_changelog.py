import pytest

from whathappened import changelog as cl


def dummy_version(ref, date, breaking, feature, fix, num_commits):
    version = cl.Version(ref, date)
    version.breaking = breaking
    version.feature = feature
    version.fix = fix
    version.commits = [None for each in range(num_commits)]

    return version


def assert_version(version_a, version_b):
    assert version_a.ref == version_b.ref
    assert version_a.date == version_b.date
    assert version_a.breaking == version_b.breaking
    assert version_a.feature == version_b.feature
    assert version_a.fix == version_b.fix
    assert len(version_a.commits) == len(version_b.commits)


@pytest.mark.parametrize(
    "test_input, expected",
    [
        (
            "performance: make it faster",
            {
                'description': 'make it faster',
                'type': 'perf',
                'scope': None,
                'is_breaking': False,
                'is_feature': False,
                'is_fix': False,
            },
        ),
        (
            "feature(read me): specify expected message format",
            {
                'description': 'specify expected message format',
                'type': 'feat',
                'scope': 'read me',
                'is_breaking': False,
                'is_feature': True,
                'is_fix': False,
            },
        ),
        (
            "features(more): all the new features",
            {
                'description': 'all the new features',
                'type': 'feat',
                'scope': 'more',
                'is_breaking': False,
                'is_feature': True,
                'is_fix': False,
            },
        ),
        (
            "Break feat(read me): specify expected message format",
            {
                'description': 'specify expected message format',
                'type': 'feat',
                'scope': 'read me',
                'is_breaking': True,
                'is_feature': True,
                'is_fix': False,
            },
        ),
        (
            "doc(README.md): specify expected message format",
            {
                'description': 'specify expected message format',
                'type': 'docs',
                'scope': 'README.md',
                'is_breaking': False,
                'is_feature': False,
                'is_fix': False,
            },
        ),
        (
            "docs(README.md): specify expected message format",
            {
                'description': 'specify expected message format',
                'type': 'docs',
                'scope': 'README.md',
                'is_breaking': False,
                'is_feature': False,
                'is_fix': False,
            },
        ),
        (
            "BREAKING fix (code): repair things",
            {
                'description': 'repair things',
                'type': 'fix',
                'scope': 'code',
                'is_breaking': True,
                'is_feature': False,
                'is_fix': True,
            },
        ),
        (
            "breaking fix: repair things",
            {
                'description': 'repair things',
                'type': 'fix',
                'scope': None,
                'is_breaking': True,
                'is_feature': False,
                'is_fix': True,
            },
        ),
        (
            "fix: add inspiration",
            {
                'description': 'add inspiration',
                'type': 'fix',
                'scope': None,
                'is_breaking': False,
                'is_feature': False,
                'is_fix': True,
            },
        ),
        (
            "fixes: add inspiration",
            {
                'description': 'add inspiration',
                'type': 'fix',
                'scope': None,
                'is_breaking': False,
                'is_feature': False,
                'is_fix': True,
            },
        ),
        (
            "docs (readme): add badges",
            {
                'description': 'add badges',
                'type': 'docs',
                'scope': 'readme',
                'is_breaking': False,
                'is_feature': False,
                'is_fix': False,
            },
        ),
        (
            "refac: add things",
            {
                'description': 'add things',
                'type': 'refactor',
                'scope': None,
                'is_breaking': False,
                'is_feature': False,
                'is_fix': False,
            },
        ),
        (
            "build(actions): create python-app.yml for github action's",
            {
                'description': 'create python-app.yml for github action\'s',
                'type': 'build',
                'scope': 'actions',
                'is_breaking': False,
                'is_feature': False,
                'is_fix': False,
            },
        ),
        (
            "README.md: correct typo",
            {
                'description': 'README.md: correct typo',
                'type': 'other',
                'scope': None,
                'is_breaking': False,
                'is_feature': False,
                'is_fix': False,
            },
        ),
        (
            "Initial commit",
            {
                'description': 'Initial commit',
                'type': 'other',
                'scope': None,
                'is_breaking': False,
                'is_feature': False,
                'is_fix': False,
            },
        ),
    ],
)
def test_commit_title_parsing(test_input, expected):
    commit = cl.Commit({'hash': '00000', 'title': test_input})

    commit_attr = {}
    for attr in expected.keys():
        commit_attr[attr] = getattr(commit, attr)

    print(commit_attr)

    assert commit_attr == expected


@pytest.mark.parametrize(
    "test_input, expected",
    [
        (
            [
                {
                    'hash': 'e324c324df48a76113ad9b3c0887f161324046e4',
                    'tags': ['v0.1.1'],
                    'author': 'Rollcloud <Rollcloud@users.noreply.github.com>',
                    'date': 'Sat Oct 17 17:30:25 2020 +0200',
                    'message': '',
                    'title': 'breaking feat(readme): specify expected message format',
                },
                {
                    'hash': '7b4e7e657f9e3f2f4033cc5f47bcc637f5799fe9',
                    'tags': [],
                    'author': 'Rollcloud <Rollcloud@users.noreply.github.com>',
                    'date': 'Sat Oct 17 15:00:48 2020 +0200',
                    'message': '',
                    'title': 'breaking fix (code): repair things',
                },
                {
                    'hash': '7b4e7e657f9e3f2f4033cc5f47bcc637f5799fe9',
                    'tags': [],
                    'author': 'Rollcloud <Rollcloud@users.noreply.github.com>',
                    'date': 'Sat Oct 17 15:00:48 2020 +0200',
                    'message': '',
                    'title': 'breaking fix: repair things',
                },
                {
                    'hash': '7b4e7e657f9e3f2f4033cc5f47bcc637f5799fe9',
                    'tags': [],
                    'author': 'Rollcloud <Rollcloud@users.noreply.github.com>',
                    'date': 'Sat Oct 17 15:00:48 2020 +0200',
                    'message': '',
                    'title': 'fix: add inspiration',
                },
                {
                    'hash': 'f60445bba0ac48e12ce6be5526644037234ae500',
                    'tags': ['v0.0.1'],
                    'author': 'Rollcloud <Rollcloud@users.noreply.github.com>',
                    'date': 'Sat Oct 17 15:00:31 2020 +0200',
                    'message': '',
                    'title': 'docs (readme): add badges',
                },
                {
                    'hash': '9e57ba91f54244af913931c017480a39605c15f9',
                    'tags': [],
                    'author': 'Rollcloud <Rollcloud@users.noreply.github.com>',
                    'date': 'Sat Oct 17 13:55:04 2020 +0200',
                    'message': (
                        'Setup Python 3.6 on ubuntu-latest\n'
                        'Install pipenv and dependencies\n'
                        'Test'
                    ),
                    'title': 'build(actions): create python-app.yml for github actions',
                },
                {
                    'hash': '4094d22846daea951c4fe0d74abb2a798e9a3404',
                    'tags': ['v0.0.0'],
                    'author': 'Rollcloud <Rollcloud@users.noreply.github.com>',
                    'date': 'Sat Oct 17 13:19:28 2020 +0200',
                    'message': '',
                    'title': 'Initial commit',
                },
            ],
            [
                dummy_version(
                    'v0.1.1',
                    'Sat Oct 17 17:30:25 2020 +0200',
                    breaking=3,
                    feature=1,
                    fix=3,
                    num_commits=4,
                ),
                dummy_version(
                    'v0.0.1',
                    'Sat Oct 17 15:00:31 2020 +0200',
                    breaking=0,
                    feature=0,
                    fix=0,
                    num_commits=2,
                ),
                dummy_version(
                    'v0.0.0',
                    'Sat Oct 17 13:19:28 2020 +0200',
                    breaking=0,
                    feature=0,
                    fix=0,
                    num_commits=1,
                ),
            ],
        )
    ],
)
def test_compile_log_versions(test_input, expected):
    commits = test_input
    versions = cl.compile_log(commits)

    for version, expectation in zip(versions, expected):
        assert_version(version, expectation)


@pytest.mark.parametrize(
    "versions, expected",
    [
        (
            [
                dummy_version(
                    'HEAD',
                    'Sat Oct 17 17:30:25 2020 +0200',
                    breaking=3,
                    feature=1,
                    fix=3,
                    num_commits=4,
                ),
                dummy_version(
                    '0.1.1',
                    'Sat Oct 17 15:00:31 2020 +0200',
                    breaking=0,
                    feature=0,
                    fix=0,
                    num_commits=2,
                ),
                dummy_version(
                    '0.0.0',
                    'Sat Oct 17 13:19:28 2020 +0200',
                    breaking=0,
                    feature=0,
                    fix=0,
                    num_commits=1,
                ),
            ],
            "0.2.0",
        ),
        (
            [
                dummy_version(
                    'HEAD',
                    'Sat Oct 17 17:30:25 2020 +0200',
                    breaking=0,
                    feature=1,
                    fix=3,
                    num_commits=4,
                ),
                dummy_version(
                    '0.1.1',
                    'Sat Oct 17 15:00:31 2020 +0200',
                    breaking=0,
                    feature=0,
                    fix=0,
                    num_commits=2,
                ),
            ],
            "0.1.2",
        ),
        (
            [
                dummy_version(
                    'HEAD',
                    'Sat Oct 17 17:30:25 2020 +0200',
                    breaking=0,
                    feature=0,
                    fix=3,
                    num_commits=4,
                ),
                dummy_version(
                    '0.1.1',
                    'Sat Oct 17 15:00:31 2020 +0200',
                    breaking=0,
                    feature=0,
                    fix=0,
                    num_commits=2,
                ),
            ],
            "0.1.2",
        ),
        (
            [
                dummy_version(
                    'HEAD',
                    'Sat Oct 17 17:30:25 2020 +0200',
                    breaking=0,
                    feature=0,
                    fix=0,
                    num_commits=4,
                ),
                dummy_version(
                    '0.1.1',
                    'Sat Oct 17 15:00:31 2020 +0200',
                    breaking=0,
                    feature=0,
                    fix=0,
                    num_commits=2,
                ),
            ],
            "0.1.1",
        ),
        (
            [
                dummy_version(
                    'HEAD',
                    'Sat Oct 17 17:30:25 2020 +0200',
                    breaking=1,
                    feature=1,
                    fix=1,
                    num_commits=4,
                ),
                dummy_version(
                    '1.0.0',
                    'Sat Oct 17 15:00:31 2020 +0200',
                    breaking=0,
                    feature=0,
                    fix=0,
                    num_commits=2,
                ),
            ],
            "2.0.0",
        ),
        (
            [
                dummy_version(
                    'HEAD',
                    'Sat Oct 17 17:30:25 2020 +0200',
                    breaking=0,
                    feature=1,
                    fix=1,
                    num_commits=4,
                ),
                dummy_version(
                    '1.0.0',
                    'Sat Oct 17 15:00:31 2020 +0200',
                    breaking=0,
                    feature=0,
                    fix=0,
                    num_commits=2,
                ),
            ],
            "1.1.0",
        ),
        (
            [
                dummy_version(
                    'HEAD',
                    'Sat Oct 17 17:30:25 2020 +0200',
                    breaking=0,
                    feature=0,
                    fix=1,
                    num_commits=4,
                ),
                dummy_version(
                    '1.0.0',
                    'Sat Oct 17 15:00:31 2020 +0200',
                    breaking=0,
                    feature=0,
                    fix=0,
                    num_commits=2,
                ),
            ],
            "1.0.1",
        ),
        (
            [
                dummy_version(
                    'HEAD',
                    'Sat Oct 17 17:30:25 2020 +0200',
                    breaking=0,
                    feature=0,
                    fix=0,
                    num_commits=4,
                ),
                dummy_version(
                    '1.0.0',
                    'Sat Oct 17 15:00:31 2020 +0200',
                    breaking=0,
                    feature=0,
                    fix=0,
                    num_commits=2,
                ),
            ],
            "1.0.0",
        ),
        (
            [
                dummy_version(
                    'HEAD',
                    'Sat Oct 17 17:30:25 2020 +0200',
                    breaking=1,
                    feature=1,
                    fix=1,
                    num_commits=4,
                ),
            ],
            "0.1.0",
        ),
    ],
)
def test_calculate_next(versions, expected):
    next_version = cl.calculate_next(versions)

    assert next_version == expected


@pytest.mark.parametrize(
    "versions, prefix, expected",
    [
        (
            [
                dummy_version(
                    'HEAD',
                    'Sat Oct 17 17:30:25 2020 +0200',
                    breaking=0,
                    feature=0,
                    fix=1,
                    num_commits=4,
                ),
                dummy_version(
                    '1.0.0',
                    'Sat Oct 17 15:00:31 2020 +0200',
                    breaking=0,
                    feature=0,
                    fix=0,
                    num_commits=2,
                ),
            ],
            "",
            "1.0.1",
        ),
        (
            [
                dummy_version(
                    'HEAD',
                    'Sat Oct 17 17:30:25 2020 +0200',
                    breaking=0,
                    feature=0,
                    fix=1,
                    num_commits=4,
                ),
                dummy_version(
                    'version1.0.0',
                    'Sat Oct 17 15:00:31 2020 +0200',
                    breaking=0,
                    feature=0,
                    fix=0,
                    num_commits=2,
                ),
            ],
            "version",
            "version1.0.1",
        ),
        (
            [
                dummy_version(
                    'HEAD',
                    'Sat Oct 17 17:30:25 2020 +0200',
                    breaking=0,
                    feature=0,
                    fix=1,
                    num_commits=4,
                ),
                dummy_version(
                    'v1.0.0',
                    'Sat Oct 17 15:00:31 2020 +0200',
                    breaking=0,
                    feature=0,
                    fix=0,
                    num_commits=2,
                ),
            ],
            "v",
            "v1.0.1",
        ),
    ],
)
def test_calculate_next_prefixes_success(versions, prefix, expected):
    next_version = cl.calculate_next(versions, prefix=prefix)

    assert next_version == expected


@pytest.mark.parametrize(
    "versions, prefix",
    [
        (
            [
                dummy_version(
                    'HEAD',
                    'Sat Oct 17 17:30:25 2020 +0200',
                    breaking=0,
                    feature=0,
                    fix=1,
                    num_commits=4,
                ),
                dummy_version(
                    '1.0.0',
                    'Sat Oct 17 15:00:31 2020 +0200',
                    breaking=0,
                    feature=0,
                    fix=0,
                    num_commits=2,
                ),
            ],
            "v",
        ),
        (
            [
                dummy_version(
                    'HEAD',
                    'Sat Oct 17 17:30:25 2020 +0200',
                    breaking=0,
                    feature=0,
                    fix=1,
                    num_commits=4,
                ),
                dummy_version(
                    'version1.0.0',
                    'Sat Oct 17 15:00:31 2020 +0200',
                    breaking=0,
                    feature=0,
                    fix=0,
                    num_commits=2,
                ),
            ],
            "version_",
        ),
        (
            [
                dummy_version(
                    'HEAD',
                    'Sat Oct 17 17:30:25 2020 +0200',
                    breaking=0,
                    feature=0,
                    fix=1,
                    num_commits=4,
                ),
                dummy_version(
                    'v1.0.0',
                    'Sat Oct 17 15:00:31 2020 +0200',
                    breaking=0,
                    feature=0,
                    fix=0,
                    num_commits=2,
                ),
            ],
            "version",
        ),
    ],
)
def test_calculate_next_prefixes_failure(versions, prefix):
    with pytest.raises(cl.VersionFormatException):
        cl.calculate_next(versions, prefix=prefix)


@pytest.mark.parametrize(
    "versions",
    [
        [
            dummy_version(
                'HEAD',
                'Sat Oct 17 17:30:25 2020 +0200',
                breaking=0,
                feature=0,
                fix=1,
                num_commits=4,
            ),
            dummy_version(
                '01.0.0',
                'Sat Oct 17 15:00:31 2020 +0200',
                breaking=0,
                feature=0,
                fix=0,
                num_commits=2,
            ),
        ],
        [
            dummy_version(
                'HEAD',
                'Sat Oct 17 17:30:25 2020 +0200',
                breaking=0,
                feature=0,
                fix=1,
                num_commits=4,
            ),
            dummy_version(
                '1.0.',
                'Sat Oct 17 15:00:31 2020 +0200',
                breaking=0,
                feature=0,
                fix=0,
                num_commits=2,
            ),
        ],
        [
            dummy_version(
                'HEAD',
                'Sat Oct 17 17:30:25 2020 +0200',
                breaking=0,
                feature=0,
                fix=1,
                num_commits=4,
            ),
            dummy_version(
                '1.0',
                'Sat Oct 17 15:00:31 2020 +0200',
                breaking=0,
                feature=0,
                fix=0,
                num_commits=2,
            ),
        ],
        [
            dummy_version(
                'HEAD',
                'Sat Oct 17 17:30:25 2020 +0200',
                breaking=0,
                feature=0,
                fix=1,
                num_commits=4,
            ),
            dummy_version(
                '1',
                'Sat Oct 17 15:00:31 2020 +0200',
                breaking=0,
                feature=0,
                fix=0,
                num_commits=2,
            ),
        ],
    ],
)
def test_calculate_next_version_string_failure(versions):
    with pytest.raises(cl.VersionFormatException):
        result = cl.calculate_next(versions)

        print(result)


@pytest.mark.parametrize(
    "versions, prefix, expected",
    [
        (
            [
                dummy_version(
                    'HEAD',
                    'Sat Oct 17 17:30:25 2020 +0200',
                    breaking=3,
                    feature=1,
                    fix=3,
                    num_commits=4,
                ),
                dummy_version(
                    'v0.1.1',
                    'Sat Oct 17 15:00:31 2020 +0200',
                    breaking=0,
                    feature=0,
                    fix=0,
                    num_commits=2,
                ),
                dummy_version(
                    'v0.0.0',
                    'Sat Oct 17 13:19:28 2020 +0200',
                    breaking=0,
                    feature=0,
                    fix=0,
                    num_commits=1,
                ),
            ],
            "v",
            [
                dummy_version(
                    'v0.2.0',
                    'Sat Oct 17 17:30:25 2020 +0200',
                    breaking=3,
                    feature=1,
                    fix=3,
                    num_commits=4,
                ),
                dummy_version(
                    'v0.1.1',
                    'Sat Oct 17 15:00:31 2020 +0200',
                    breaking=0,
                    feature=0,
                    fix=0,
                    num_commits=2,
                ),
                dummy_version(
                    'v0.0.0',
                    'Sat Oct 17 13:19:28 2020 +0200',
                    breaking=0,
                    feature=0,
                    fix=0,
                    num_commits=1,
                ),
            ],
        )
    ],
)
def test_update_latest_version(versions, prefix, expected):
    versions = cl.update_latest_version(versions, prefix=prefix)

    for version, expectation in zip(versions, expected):
        assert_version(version, expectation)


@pytest.mark.parametrize(
    "test_input, expected",
    [
        (
            [
                {
                    'hash': 'e324c324df48a76113ad9b3c0887f161324046e4',
                    'tags': ['v0.1.1'],
                    'author': 'Rollcloud <Rollcloud@users.noreply.github.com>',
                    'date': 'Sat Oct 17 17:30:25 2020 +0200',
                    'message': '',
                    'title': 'breaking feat(readme): specify expected message format',
                },
                {
                    'hash': '7b4e7e657f9e3f2f4033cc5f47bcc637f5799fe9',
                    'tags': [],
                    'author': 'Rollcloud <Rollcloud@users.noreply.github.com>',
                    'date': 'Sat Oct 17 15:00:48 2020 +0200',
                    'message': '',
                    'title': 'breaking fix (code): repair things',
                },
                {
                    'hash': '7b4e7e657f9e3f2f4033cc5f47bcc637f5799fe9',
                    'tags': [],
                    'author': 'Rollcloud <Rollcloud@users.noreply.github.com>',
                    'date': 'Sat Oct 17 15:00:48 2020 +0200',
                    'message': '',
                    'title': 'breaking fix: repair things',
                },
                {
                    'hash': '7b4e7e657f9e3f2f4033cc5f47bcc637f5799fe9',
                    'tags': [],
                    'author': 'Rollcloud <Rollcloud@users.noreply.github.com>',
                    'date': 'Sat Oct 17 15:00:48 2020 +0200',
                    'message': '',
                    'title': 'fix: add inspiration',
                },
                {
                    'hash': 'f60445bba0ac48e12ce6be5526644037234ae500',
                    'tags': ['v0.0.1'],
                    'author': 'Rollcloud <Rollcloud@users.noreply.github.com>',
                    'date': 'Sat Oct 17 15:00:31 2020 +0200',
                    'message': '',
                    'title': 'docs (readme): add badges',
                },
                {
                    'hash': '9e57ba91f54244af913931c017480a39605c15f9',
                    'tags': [],
                    'author': 'Rollcloud <Rollcloud@users.noreply.github.com>',
                    'date': 'Sat Oct 17 13:55:04 2020 +0200',
                    'message': (
                        'Setup Python 3.6 on ubuntu-latest\n'
                        'Install pipenv and dependencies\n'
                        'Test'
                    ),
                    'title': 'build(actions): create python-app.yml for github actions',
                },
                {
                    'hash': '4094d22846daea951c4fe0d74abb2a798e9a3404',
                    'tags': ['v0.0.0'],
                    'author': 'Rollcloud <Rollcloud@users.noreply.github.com>',
                    'date': 'Sat Oct 17 13:19:28 2020 +0200',
                    'message': '',
                    'title': 'Initial commit',
                },
            ],
            """# Changelog

## v0.1.1 (2020-10-17)

### Features

* Readme - specify expected message format [BREAKING]

### Fixes

* Add inspiration
* Repair things [BREAKING]
* Code - repair things [BREAKING]


## v0.0.1 (2020-10-17)

### Docs

* Readme - add badges


## v0.0.0 (2020-10-17)

### Other

* Initial commit
""",
        )
    ],
)
def test_changelog(test_input, expected):
    commits = test_input
    versions = cl.compile_log(commits)
    log = cl.format_log(versions)

    print(log)

    assert log == expected
