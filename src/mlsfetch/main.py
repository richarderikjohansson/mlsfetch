import argparse
import earthaccess
from .runner import MLSRuntime


def auth():
    parser = argparse.ArgumentParser(
        add_help=True,
        description="Runtime tool to search and download MLS data"
    )
    parser.add_argument(dest="login",
                        help="Login to your EDL account",
                        default=True)
    parser.add_argument("--persist",
                        help="Save login credentials in a .netrc file",
                        action="store_true")
    args = parser.parse_args()

    if args.login:
        if args.persist:
            edl = earthaccess.login(persist=True)
        else:
            edl = earthaccess.login()

    assert edl.authenticated, "Login failed, look into credentials"
    shell = MLSRuntime(edl=edl)
    shell.cmdloop()


#if __name__ == "__main__":
#    auth()
