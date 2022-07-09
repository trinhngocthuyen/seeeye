#!/bin/bash
set -e

cd examples/ios

bundle install
bundle exec pod install

python3 -m cicd.ios.build --derived-data-path DerivedData
python3 -m cicd.ios.test --derived-data-path DerivedData --test-without-building
