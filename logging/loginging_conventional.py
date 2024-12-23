import logging

logger = logging.getLogger("my_app")


def main():
    logging.basicConfig(level="DEBUG")
    logger.debug("debug message")
    logger.info("info message")
    logger.warning("warning message")
    logger.error("error messgae")
    logger.critical("critical message")

    try:
        1 / 0
    except ZeroDivisionError:
        logger.exception("exception message")


if __name__ == "__main__":
    main()
