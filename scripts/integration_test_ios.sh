#!/bin/bash
set -e

cd examples/ios

bundle install

python3 -m cicd.ios.build \
    --cocoapods \
    --build-for-testing
python3 -m cicd.ios.test \
    --test-without-building
