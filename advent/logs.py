import logging


def setup_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s][%(levelname)-7s][%(name)s] %(message)s",
    )
    logging.getLogger("__main__").setLevel(logging.DEBUG)
    logging.getLogger("advent").setLevel(logging.DEBUG)
