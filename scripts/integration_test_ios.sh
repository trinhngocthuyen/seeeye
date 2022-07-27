#!/bin/bash
set -e

cd examples/ios
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
        --derived-data-path DerivedData \
        --test-without-building
}

function _exec_coverage() {
    echo "To be implemented"
}

if [[ -z ${ACTION} ]]; then
    actions=(build test coverage)
else
    actions=(${ACTION})
fi

for action in ${actions[@]}; do
    eval "_exec_${action}"
done
