#!/usr/bin/env bash

LATEST_PGS_TO_SRT_VERSION=$(curl -s https://api.github.com/repos/Tentacule/PgsToSrt/releases/latest | grep -oP '"tag_name": "\K(.*)(?=")')
WITHOUT_V=$(echo $LATEST_PGS_TO_SRT_VERSION | sed 's/v//')

rm PgsToSrt-$WITHOUT_V.zip

wget https://github.com/Tentacule/PgsToSrt/releases/download/$LATEST_PGS_TO_SRT_VERSION/PgsToSrt-$WITHOUT_V.zip
unzip PgsToSrt-$WITHOUT_V.zip -d PgsToSrtWrapper/PgsToSrt

sudo dnf install tesseract
