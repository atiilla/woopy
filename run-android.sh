#!/bin/bash

pushd store || exit
alias woopygui-android='briefcase create android && briefcase build android && briefcase run android'
woopygui-android
popd || exit