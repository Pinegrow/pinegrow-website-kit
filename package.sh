#!/bin/bash
# Makes the downloads from the last commit (see .gitattributes for what they contain):
#   pinegrow-website-kit-<version>-static.zip     without the WordPress attributes and templates
#   pinegrow-website-kit-<version>-wordpress.zip  the kit as it is in this repository
#   kit-builder-skill.zip                          only the skill, as the folder pinegrow-website-kit. Upload it to
#                                                  every release under this name: Kit Builder prompts download it from
#                                                  releases/latest/download/kit-builder-skill.zip
# Usage: ./package.sh 1.1
set -euo pipefail
cd "$(dirname "$0")"
version="${1:?Give the version, for example: ./package.sh 1.1}"
# Untracked files never get into the zips (git archive), so only uncommitted changes stop it.
if [ -n "$(git status --porcelain --untracked-files=no)" ]; then
    echo "Commit your changes first; the zips are made from the last commit:"
    git status --short --untracked-files=no
    exit 1
fi

dist="$HOME/Documents/PinegrowDist"
mkdir -p "$dist"
work="$(mktemp -d)"
trap 'rm -rf "$work"' EXIT

for variant in static wordpress; do
    mkdir -p "$work/$variant/pinegrow-website-kit"
    git archive HEAD | tar -x -C "$work/$variant/pinegrow-website-kit"
    python3 tools/make_variant.py "$variant" "$work/$variant/pinegrow-website-kit"
    out="$dist/pinegrow-website-kit-$version-$variant.zip"
    rm -f "$out"
    (cd "$work/$variant" && zip -qrX "$out" pinegrow-website-kit)
    echo "$out ($(du -h "$out" | cut -f1))"
done

mkdir -p "$work/skill"
git archive HEAD kit-builder | tar -x -C "$work/skill"
mv "$work/skill/kit-builder" "$work/skill/pinegrow-website-kit"
out="$dist/kit-builder-skill.zip"
rm -f "$out"
(cd "$work/skill" && zip -qrX "$out" pinegrow-website-kit)
echo "$out ($(du -h "$out" | cut -f1))"
