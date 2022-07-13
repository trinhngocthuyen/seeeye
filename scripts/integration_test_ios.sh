#!/bin/bash
set -e

cd examples/ios

bundle install
bundle exec pod install

python3 -m cicd.ios.build --build-for-testing
python3 -m cicd.ios.test --test-without-building
