#!/bin/bash

alias crenv='python -m venv .venv'
alias acenv='source .venv/Scripts/activate'
alias upenv='python -m pip install --upgrade pip'
alias insenv='upenv && pip3 install toga python-dotenv requests briefcase'
alias deenv='source .venv/Scripts/deactivate'
alias bc='python -m briefcase'
alias bc-new='bc new'
alias bc-and='bc create android && bc build android && bc run android'
alias bc-ios='bc create ios && briefcase build ios && bc run ios'
alias bc-mac='bc create macos && bc build macos && bc run macos'
alias bc-win='bc create windows && bc build windows && bc run windows'
alias bc-lin='bc create linux && bc build linux && bc run linux'
alias bc-web='bc create web && bc build web && bc run web'
alias bc-clean='rm -rf .venv && rm -rf .briefcase && rm -rf .build && rm -rf .dist && rm -rf .ios'

