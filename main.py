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

def main():
    parser = argparse.ArgumentParser(usage= "your@email.com [folder to scan]")
    parser.add_argument("-add", "--folder", help="add a new folder to scan for Git repositories")
    parser.add_argument("-email", help="the email to scan")
    parser.add_argument("-date", "--StartingDate", help="the date to start the scanning")
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

    stats(args.email, )

main()

