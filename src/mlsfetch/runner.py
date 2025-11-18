import cmd
from .main import earthaccess
from pathlib import Path
from datetime import datetime
from .log import get_download_logger, get_runtime_logger

PRODUCT = {
    "O3": "ML2O3",
    "H2O": "ML2H2O",
    "CO": "ML2CO",
    "CH3CN": "ML2CH3CN",
    "N2O": "ML2N2O",
    "ClO": "ML2ClO",
    "HNO3": "ML2HNO3",
    "HOCl": "ML2HOCl",
    "T": "ML2T",
}


class MLSRuntime(cmd.Cmd):
    def __init__(self, edl):
        super().__init__()
        self.username = edl.username
        self.auth = edl.authenticated
        self.prompt = f"{self.username}: "
        self.rlogger = get_runtime_logger()
        self.intro = f"Welcome {
            self.username
        } to MLS search and download tool. Type help or ? to list commands\n"

    def do_exit(self, arg):
        "Exit MLS search and download tool"

        self.rlogger.info(f"Exiting for {self.username}")
        return True

    def do_search(self, arg):
        """
        Search for MLS datasets.
        Products available:
        O3
        H2O
        CO
        CH3CN
        N2O
        ClO
        HNO3
        HOCl
        T

        positional argument:
        product    Product to search after
        year       For which year you want to download the data
        """
        args = arg.split()

        self.product = args[0]
        self.year = args[1]
        self.short_name = check_product(product=self.product)

        if self.year == "__all__":
            temporal = "2004"
        else:
            check_year(self.year, self.rlogger)
            temporal = (self.year, self.year)

        if self.short_name is not None:
            self.rlogger.info(f"Started search for {self.product}")
            self.results = earthaccess.search_data(
                short_name=self.short_name,
                version="005",
                temporal=temporal,
                bounding_box=(-180, -82, 180, 82),  # global coverage
                count=-1,
            )
        else:
            msg = f"{self.product} is not a MLS product"
            self.rlogger.error(msg)

    def do_list(self, arg):
        if hasattr(self, "results"):
            for granule in self.results:
                nativeid = granule["meta"]["native-id"]
                file = nativeid.split(":")[-1]
                self.rlogger.info(file)
        else:
            msg = "You need to search for data before listing them."
            self.rlogger.error(msg)

    def do_download(self, arg):
        """
        Download datasets into $HOME/MLS.
        """
        if hasattr(self, "results"):
            home = Path.home()
            savedir = home / "MLS" / self.product

            if not savedir.exists():
                savedir.mkdir(parents=True)

            dlogger = get_download_logger(home / "MLS")
            files = earthaccess.download(self.results, local_path=savedir)

            dlogger.info("Downloaded:\n")
            for file in files:
                dlogger.info(file)
        else:
            msg = "You need to search for data before downloading."
            self.rlogger.error(msg)


def check_year(year, logger):
    try:
        datetime.strptime(year, "%Y")
    except ValueError:
        logger.error("Check format of 'year', has to be YYYY")


def check_product(product):
    try:
        short_name = PRODUCT[product]
        return short_name
    except KeyError:
        return None
