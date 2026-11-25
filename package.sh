#!/bin/bash
# Makes the download zip from the last commit: README.md, website/ and kit-builder/ (see .gitattributes).
# Usage: ./package.sh 1.0
set -euo pipefail
cd "$(dirname "$0")"
version="${1:?Give the version, for example: ./package.sh 1.0}"
if [ -n "$(git status --porcelain)" ]; then
    echo "Commit your changes first; the zip is made from the last commit:"
    git status --short
    exit 1
fi
out="$HOME/Documents/PinegrowDist/pinegrow-website-kit-$version.zip"
mkdir -p "$(dirname "$out")"
git archive --format=zip --prefix="pinegrow-website-kit/" -o "$out" HEAD
echo "$out ($(du -h "$out" | cut -f1))"
