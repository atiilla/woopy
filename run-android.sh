#!/bin/bash

pushd store || exit
briefcase run android -d "@beePhone"
popd || exit