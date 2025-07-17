import argparse
import scan as sc
import stats as st

def listFolders():
    sc.listFolders()

def remove(folder: str):
    sc.RemoveFolder(folder)

def scan(folder: str):
    sc.scan(folder)

def stats(email: str):
    st.stats(email)

def statsDate(email: str, date: str):
    st.statsDate(email, date)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-add", "--folder", help="add a new folder to scan for Git repositories")
    parser.add_argument("-email", help="the email to scan")
    parser.add_argument("-date", "--startingdate", help="dd/mm/yyyy")
    parser.add_argument("-ls", "--list", help="List the folders that is being checked", action="store_true")
    parser.add_argument("-rm", "--remove", help="Remove the folder")
    args = parser.parse_args()
    if args.list:
        listFolders()
        return
    if args.remove:
        remove(args.remove)
        return
    if args.folder:
        scan(args.folder)
        return
    if args.email:
        if args.startingdate:
            statsDate(args.email, args.startingdate)
            return
        stats(args.email)
        return
    parser.print_help()

main()

