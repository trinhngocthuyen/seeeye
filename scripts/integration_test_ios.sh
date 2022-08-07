#!/bin/bash
set -e

cd examples/ios
mkdir -p tmp && printf 0 > tmp/test_retries_trace # To simulate test retries

bundle install
bundle exec pod install

common_args=(
    --derived-data-path DerivedData
)

function _exec_build() {
    python3 -m cicd.ios.cli build \
        ${common_args[@]} \
        --build-for-testing
}

function _exec_test() {
    if [[ ! -z ${ONLY_TESTING} ]]; then
        only_testing_args=(
            --only-testing ${ONLY_TESTING}
        )
    fi
    python3 -m cicd.ios.cli test \
        ${common_args[@]} \
        ${only_testing_args[@]} \
        --retries 1 \
        --shards 2 \
        --shard-idx ${SHARD_IDX:-0} \
        --test-without-building
}

function _exec_coverage() {
    python3 -m cicd.ios.cli cov \
        ${common_args[@]}
}

if [[ -z ${ACTION} ]]; then
    actions=(build test coverage)
else
    actions=(${ACTION})
fi

for action in ${actions[@]}; do
    eval "_exec_${action}"
done
