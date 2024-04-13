#!/bin/bash

pushd store || exit
alias crenv='python3.8 -m venv .venv'
alias acenv='source .venv/bin/activate'
alias insenv='pip3 install -r requirements.txt'
alias deenv='source .venv/bin/deactivate'
alias woopygui-android='briefcase create android && briefcase build android && briefcase run android'
alias woopygui-ios='briefcase create ios && briefcase build ios && briefcase run ios'
alias woopygui-macos='briefcase create macos && briefcase build macos && briefcase run macos'
alias woopygui-windows='briefcase create windows && briefcase build windows && briefcase run windows'
alias woopygui-linux='briefcase create linux && briefcase build linux && briefcase run linux'
alias woopygui-web='briefcase create web && briefcase build web && briefcase run web'
alias woopygui-all='woopygui-android && woopygui-ios && woopygui-macos && woopygui-windows && woopygui-linux && woopygui-web'
popd || exit
