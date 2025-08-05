import cmd
from .main import earthaccess
from pathlib import Path
from datetime import datetime

PRODUCT = {
    "O3": "ML2O3",
    "H20": "ML2H2O",
    "CO": "ML2CO",
    "CH3CN": "ML2CH3CN",
    "N2O": "ML2N2O",
    "ClO": "ML2ClO",
    "HNO3": "ML2HNO3",
    "HOCl": "ML2HOCl",
    "T": "ML2T"
}


class MLSRuntime(cmd.Cmd):
    def __init__(self, edl):
        super().__init__()
        self.username = edl.username
        self.auth = edl.authenticated
        self.prompt = f"{self.username}: "
        self.intro = f"Welcome {self.username} to MLS search and download tool. Type help or ? to list commands\n"

    def do_exit(self, arg):
        "Exit MLS search and download tool"

        # logging, instead?
        print(f"Thank you and goodbye {self.username}")
        return True

    def do_search(self, arg):
        """
        Search for MLS datasets.
        Products available:
        O3
        H20
        CO
        CH3CN
        N2O
        ClO
        HNO3
        HOCl

        positional argument:
        product    Product to search after
        year       For which year you want to download the data
        """
        args = arg.split()

        self.product = args[0]
        self.year = args[1]
        self.short_name = check_product(product=self.product)

        if self.year == "__all__":
            temporal = ("2004")
        else:
            check_year(self.year)
            temporal = (self.year, self.year)

        self.results = earthaccess.search_data(
            short_name=self.short_name,
            version="005",
            temporal=temporal,
            bounding_box=(-180, -82, 180, 82),  # global coverage
            count=-1
        )

    def do_list(self, arg):
        if hasattr(self, "results"):
            dsets = earthaccess.open(self.results)
            for ds in dsets:
                print(ds)
        else:
            print("You need to search for data before listing them. See help search")

    def do_download(self, arg):
        """
        Download datasets into $HOME/MLS.
        """
        if hasattr(self, "results"):
            home = Path.home()
            savedir = home / "MLS" / self.product
            earthaccess.download(self.results, local_path=savedir)
        else:
            print("You need to search for data before downloading. See 'help download'")


def check_year(year):
    try:
        datetime.strptime(year, "%Y")
    except ValueError:
        print("Check year, has to be for example '2024' for 2024")


def check_product(product):
    try:
        short_name = PRODUCT[product]
        return short_name
    except KeyError:
        print(f"'{product}' is not a MLS product. Type 'help search' to see the products")
