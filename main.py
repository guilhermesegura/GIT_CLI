import argparse
import scan as sc
import stats as st

def scan(folder: str):
    sc.scan(folder)

def stats(email: str):
    st.stats(email)

def main():
    parser = argparse.ArgumentParser(usage= "your@email.com [folder to scan]")
    parser.add_argument("-add", "--folder", help="add a new folder to scan for Git repositories")
    parser.add_argument("-email", help="the email to scan")
    parser.add_argument("-date", "--StartingDate", help="the date to start the scanning")
    args = parser.parse_args()
    if args.folder:
        scan(args.folder)
        return

    stats(args.email, )

main()

