# Fastapi deployment

## To run locally

1. Put desired mlem model to directory fastapi-deployment/art_model. Model should be namend just `model`

2. Install dependencies

```sh
$ poetry install
```

3. Run server

```sh
$ poetry run python serve_with_monitoring.py
```


## To deploy on fly.io:

1. Pack and upload your mlem model to transfer.sh. Script will return link to archive. Model should be namend just `model`
```sh
$ ./upload_model.sh <YOUR_MODEL_DIR>
```

3. Deploy

```sh
$ flyctl deploy --build-arg MODEL_ARCHIVE_LINK=<YOUR_MODEL_ARCHIVE_LINK>
```
