import datetime as dt

import typer

from hedera.config import settings
from hedera.records.downloader import RecordFileDownloader
from hedera.records.orchestrator import RecordFileOrchestrator

dt_fmt: str = "%Y-%m-%dT%H:%M:%S.%f"

app = typer.Typer()
default_now = dt.datetime.strftime(dt.datetime.utcnow(), dt_fmt)


@app.command()
def record_file_downloader(
    network: str = "mainnet", directory: str = ".", log_level: str = settings.LOG_LEVEL, backfill_marker: str = None
):
    cli_options = {"network": network, "log_dir": directory, "log_level": log_level, "backfill_marker": backfill_marker}

    rfd = RecordFileDownloader(cli_options)
    rfd.run()


@app.command()
def record_file_orchestrator(
    network: str = "mainnet", directory: str = ".", log_level: str = settings.LOG_LEVEL, backfill_marker: str = None
):

    cli_options = {"network": network, "log_dir": directory, "log_level": log_level, "backfill_marker": backfill_marker}

    rfo = RecordFileOrchestrator(cli_options)
    rfo.run()


if __name__ == "__main__":
    app()
