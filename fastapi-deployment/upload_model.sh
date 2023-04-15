#!/usr/bin/env bash
set -e

TARGET_PATH=$1

MLEM_FILE=$TARGET_PATH/model.mlem
if  test ! -f "$MLEM_FILE"; then
    echo "mlem file should exist at $MLEM_FILE"
    exit 1
fi

MODEL_DIR=$TARGET_PATH/model
if  test ! -d "$MODEL_DIR"; then
    echo "model dir should exist at $MODEL_DIR"
    exit 1
fi


ARCHIVE_PATH="model.tar.gz"


tar -C $TARGET_PATH -czvf $ARCHIVE_PATH model model.mlem
echo Model archive created at $ARCHIVE_PATH

FILE_LINK=$(curl --upload-file $ARCHIVE_PATH https://transfer.sh/$ARCHIVE_PATH)
echo model uploaded to $FILE_LINK
