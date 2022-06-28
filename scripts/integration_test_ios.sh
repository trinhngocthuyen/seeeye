#!/bin/bash
set -e

cd examples/ios

bundle install
bundle exec pod install

python3 -m cicd.ios.build
python3 -m cicd.ios.test
