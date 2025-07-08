import argparse
import logging
import sys

from cli.invoker import CLIInvoker

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,  # Può essere DEBUG, WARNING, ERROR, ecc.
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def main():
    args = sys.argv[1:]

    invoker = CLIInvoker()

    try:
        invoker.set_command(args)
        invoker.run_command()
    except Exception as e:
        logger.error(f"❌ Error: {e}\n")


if __name__ == "__main__":
    main()
