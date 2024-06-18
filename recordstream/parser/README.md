
# Recordstream Parser

This repository contains scripts and pipeline configurations to ingest Hedera data. These services function as a private mirror node, exposing data on the Hedera ledger.

## Hedera Ledger Ingestion Services

The ingestion process involves downloading files from a node's Google bucket and storing them in a local directory. A parser (orchestrator.py) then processes these files, decodes them, parses the data, and writes the parsed output to a file.

### Components

1. **Records Downloader**
   - **Path:** `hedera/records/downloader.py`
   - **Function:** Downloads files from a node's Google bucket and saves them in a local directory.

2. **Records Orchestrator**
   - **Path:** `hedera/records/orchestrator.py`
   - **Function:** Picks up the downloaded files, decodes them, parses the data, and writes the parsed output to a JSON file.

## Local Environment

To run the Hedera repository locally, follow these steps:

1. **Clone the Hedera Repository**
   ```bash
   git clone https://github.com/hashgraph/elasticsearch-assets.git
   cd elasticsearch-assets
   ```

2. **Create a `.env` File**
   
   Set up your local environment by creating a `.env` file in the project root. Contact the Hedera team to obtain the necessary connection credentials and external datasource details. Here’s an example `.env` file:

   ```dotenv
   # .env
   HEDERA_APP_PATH=$DIRECTORY/elasticsearch-assets/recordstream/parser/
   HEDERA_SCRIPTS_PATH=$DIRECTORY/elasticsearch-assets/recordstream/parser/hedera
   HEDERA_DEV_ENV=True
   LOG_DIR=$DIRECTORY/elasticsearch-assets/recordstream/parser/logs
   PARSER_OUTPUT_DIR=$DIRECTORY/elasticsearch-assets/recordstream/parser/outputs

   # Downloaders and Loggers
   GOOGLE_APP_CREDENTIALS=$DIRECTORY/hedera-dev/hedera/mainnet-exports-4e9696cee502.json
   HEDERA_BUCKET_NAME=hedera-mainnet-streams
   HEDERA_BUCKET_NODE=0.0.3
   RECORDS_BUCKET_PREFIX=recordstreams/record0.0.3/
   RECORDS_FILE_EXTENSION=rcd
   RECORDS_FILES_PATH=$DIRECTORY/MirrorNodeData/recordstreams/
   PARSED_RECORD_STREAM_FILES_DIR=parsedRecordStreamFiles
   PARSED_RECORD_STREAM_FILES_PATH=$DIRECTORY/MirrorNodeData/recordstreams/parsedRecordStreamFiles/
   ```

3. **Ensure Python 3.9.x is Installed**
   ```bash
   python3 --version
   ```

4. **Ensure Poetry 1.2.x is Installed**
   ```bash
   poetry -v
   ```

5. **Install Packages with Poetry**
   ```bash
   poetry install
   ```

6. **Download Record Files from Hedera's Google Bucket**
   
   Use the following command to download record files. The downloaded files will be stored in the `RECORDS_FILES_PATH` directory.
   ```bash
   poetry run record-file-downloader
   ```

7. **Parse Record Files**
   
   Parse the downloaded record files using the command below. The processed files will have a `processed` suffix and will be stored in the `PARSED_RECORD_STREAM_FILES_PATH` directory. The parsed output will be saved as JSON files in the `PARSER_OUTPUT_DIR` directory.
   ```bash
   poetry run record-file-orchestrator
   ```

## Backfilling Missing Data

If there is a bug in a parser or any downtime, backfilling data might be necessary to recover the missed data during an outage. All Hedera ledger ingestion services support a "backfill" mode for this purpose. Below is a guide on how to backfill missing data. Note that backfilling may require a dedicated VM connected to Elasticsearch; the SRE team can assist with this setup if needed.

### Steps for Backfilling Data

1. **Download the Missing Files**
   - Use the following command to download files from the timeframe where data was not collected or was erroneous:
     ```bash
     poetry run python hedera/cli.py record-file-downloader --backfill-marker "<pattern>"
     ```
   - The `backfill-marker` parameter specifies the location/filenames (time-based) to collect from the Google bucket. Hedera's files follow this format: `YYYY-MM-DDTHH_mm_ss`.
   - Ensure the downloader targets an online node to prevent the marker from resetting.

2. **Parse the Missing Files**
   - Use the following command to parse the downloaded files:
     ```bash
     poetry run python hedera/cli.py record-file-orchestrator --backfill-marker "<pattern>"
     ```
   - The `marker` parameter specifies the local directory where the files have been downloaded. Use the format: `YYYY-MM-DD`.