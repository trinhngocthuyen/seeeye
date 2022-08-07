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
    local args=()
    if [[ ! -z ${ONLY_TESTING} ]]; then
        args+=(--only-testing ${ONLY_TESTING})
    fi
    if [[ ! -z ${NUM_OF_SHARDS} ]]; then
        args+=(
            --shards ${NUM_OF_SHARDS}
            --shard-idx ${SHARD_IDX:-0}
        )
    fi
    python3 -m cicd.ios.cli test \
        ${common_args[@]} \
        ${args[@]} \
        --retries 1 \
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
