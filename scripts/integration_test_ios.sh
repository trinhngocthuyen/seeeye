#!/bin/bash
set -e

if [[ ! -d integration_tests ]]; then
    git submodule sync
    git submodule update --init
fi

cd integration_tests
mkdir -p tmp && printf 0 > tmp/test_retries_trace # To simulate test retries

bundle install
bundle exec pod install

function _exec_build() {
    python3 -m cicd.ios.build \
        --derived-data-path DerivedData \
        --build-for-testing
}

function _exec_test() {
    python3 -m cicd.ios.test \
        --retries 1 \
        --shards 2 \
        --shard-idx ${SHARD_IDX:-0} \
        --derived-data-path DerivedData \
        --test-without-building
}

function _exec_coverage() {
    # TODO: Replace implementation
    echo "check files..." && find DerivedData
    mkdir -p /tmp
    curl -s https://codecov.io/bash -o /tmp/codecov.sh
    local commit_sha=$(git show --no-patch --format="%P")
    local repo_slug="trinhngocthuyen/seeeye-integration-test"
    env GITHUB_SHA=${commit_sha} \
        GITHUB_REPOSITORY=${repo_slug} \
        GITHUB_HEAD_REF="" \
        sh /tmp/codecov.sh \
            -D DerivedData \
            -r ${repo_slug}
}

if [[ -z ${ACTION} ]]; then
    actions=(build test coverage)
else
    actions=(${ACTION})
fi

for action in ${actions[@]}; do
    eval "_exec_${action}"
done
