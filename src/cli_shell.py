import logging
from cli.invoker import CLIInvoker

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,  # Può essere DEBUG, WARNING, ERROR, ecc.
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def cli_shell():
    print("🛠️ Smart Contract Analyzer (CLI Mode)\nType 'help' for a list of commands. Type 'exit' to quit.\n")

    invoker = CLIInvoker()

    while True:
        try:
            user_input = input(">>> ").strip()
            if not user_input:
                continue
            if user_input.lower() in ["exit", "quit"]:
                logger.info("👋 Exiting.")
                break

            args = user_input.split()

            invoker.set_command(args)
            invoker.run_command()

        except SystemExit:
            # Intercetta le eccezioni da argparse (argomenti errati)
            print('\n')
        except KeyboardInterrupt:
            logger.info("\n👋 Exiting.")
            break
        except Exception as e:
            logger.error(f"❌ Error: {e}\n")


if __name__ == "__main__":
    cli_shell()
