# Base Processor

This repository builds the following ETL base processor images:

```
pennsieve/etl-base-processor
pennsieve/etl-base-processor-test
pennsieve/base-processor-freesurfer
pennsieve/base-processor-freesurfer-test
pennsieve/base-processor-pandas
pennsieve/base-processor-pandas-test
pennsieve/base-processor-java-python
```

## Update processor's base docker image

Esure you have your `PENNSIEVE_CODE_DIR` env var set (this is where all of your GitHub repos should be located locally).

Usage:
```shell
./update_processors_base.sh <new_tag>
```

Example:
```shell
./update_processor_base.sh 2-zxzcv
