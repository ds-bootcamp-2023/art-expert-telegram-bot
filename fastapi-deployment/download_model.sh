#!/usr/bin/env bash
set -e

MODEL_ARCHIVE_URL=$1

ARCHIVE_FILENAME="art_model.tar.gz"

curl $MODEL_ARCHIVE_URL --output $ARCHIVE_FILENAME

TARGET_MODEL_DIR=art_model

mkdir $TARGET_MODEL_DIR
tar -xvzf $ARCHIVE_FILENAME -C $TARGET_MODEL_DIR


MLEM_FILE=$TARGET_MODEL_DIR/model.mlem
if  test ! -f "$MLEM_FILE"; then
    echo "Model archive format invalid: mlem file should exist at $MLEM_FILE"
    exit 1
fi

MODEL_DIR=$TARGET_MODEL_DIR/model
if  test ! -d "$MODEL_DIR"; then
    echo "Model archive format invalid: model dir should exist at $MODEL_DIR"
    exit 1
fi

rm $ARCHIVE_FILENAME