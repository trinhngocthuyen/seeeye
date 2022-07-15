#!/bin/bash
set -e

cd examples/ios
mkdir -p tmp && printf 0 > tmp/test_retries_trace # To simulate test retries

bundle install

python3 -m cicd.ios.build \
    --cocoapods \
    --derived-data-path DerivedData \
    --build-for-testing
python3 -m cicd.ios.test \
    --retries 1 \
    --derived-data-path DerivedData \
    --test-without-building
