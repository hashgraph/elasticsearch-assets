import logging


def hedera_logger(level, handlers=None, filename=None):
    if handlers is not None:
        logging.basicConfig(
            handlers=handlers,
            level=level,
            format="%(asctime)s.%(msecs)03d %(levelname)s: %(message)s",
        )
    if filename is not None:
        logging.basicConfig(
            filename=filename,
            level=level,
            format="%(asctime)s.%(msecs)03d %(levelname)s: %(message)s",
        )
    hedera_logger = logging.getLogger(__name__)

    return hedera_logger
