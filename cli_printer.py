import logging
from colorama import Fore, Style, init

# Initialize colorama for Windows
init(autoreset=True)

# Setup Logger
logging.basicConfig(
    filename="log.txt",
    filemode="a",
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
)


def print_header(title):
    print(f"\n{Fore.CYAN}{'='*60}")
    print(f"{Fore.YELLOW}{title}")
    print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")


def print_success(msg):
    print(f"{Fore.GREEN}✔ {msg}{Style.RESET_ALL}")
    logging.info(msg)


def print_error(msg):
    print(f"{Fore.RED}✘ {msg}{Style.RESET_ALL}")
    logging.error(msg)


def print_warning(msg):
    print(f"{Fore.YELLOW}⚠ {msg}{Style.RESET_ALL}")
    logging.warning(msg)


def print_company_header(name, company_id, count, total):
    print(f"\n{Fore.CYAN}Processing [{count}/{total}]: "
          f"{Fore.WHITE}{name} ({company_id}){Style.RESET_ALL}")
    logging.info(f"Processing {name} ({company_id})")


def print_pros_cons(pros, cons):
    print(f"{Fore.GREEN}\nTop Pros:{Style.RESET_ALL}")
    for p in pros:
        print(f"   {Fore.GREEN}+ {p}")

    print(f"{Fore.RED}\nTop Cons:{Style.RESET_ALL}")
    for c in cons:
        print(f"   {Fore.RED}- {c}")
