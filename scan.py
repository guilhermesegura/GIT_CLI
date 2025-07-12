import os

def scan(folder: str):
    print("Found folders:\n")
    
    repositories =  recursiveScanFolder(folder)
    filePath = getDotFilePath()
    addNewListElementsToFile(filePath, repositories)
    print("\n\nSuccessfully added\n\n")

def scanGitFolders(folders : list[str], folder : str) -> list[str]:
    folder = folder.rstrip("/\\")
    for file in os.scandir(folder):    
        try:
            is_dir = file.is_dir(follow_symlinks=False)
        except OSError as error:
            print('Error calling is_dir():', error)
            continue
        if is_dir:
            path = folder + "/" + file.name
            if file.name == ".git":
                path = path.rstrip("/.git")
                print(path)
                path = os.path.normpath(path)
                folders.append(path)
                continue
            if file.name == "vendor" or file.name == "node_modules":
                continue

            folders = scanGitFolders(folders, path)
    return folders

def recursiveScanFolder(folder: str) -> list[str]:
    return scanGitFolders([], folder)

def getDotFilePath() -> str:
    dotFile = os.path.expanduser("~") + "/.pygitlocalstats"
    dotFile = os.path.normpath(dotFile)
    return dotFile

def addNewListElementsToFile(filePath: str, newRepos: list[str]):
    existingRepos = parseFileLinesToLists(filePath)
    repos = joinLists(newRepos, existingRepos)
    dumpStringsListToFile(repos, filePath)

def parseFileLinesToLists(filepath: str) ->list[str]:
    lines = []
    if not os.path.exists(filepath):
        with open(filepath, "w"):
            pass
    else:
        with open(filepath, "r") as f:
             for line in f:
                lines.append(line)
 
    return lines

def joinLists(new: list[str], existing: list[str])-> list[str]:
    auxiliarSet = set(existing)
    for entry in new:
        if entry not in auxiliarSet:
            existing.append(entry)
    return existing

def dumpStringsListToFile(repos: list[str], filePath: str):
    content = "\n".join(repos)
    with open(filePath, "w") as f:
        f.write(content)

def printRepos(repos: list[str]):
    print("\n List of Repositories that are being used: \n")
    for i, n in enumerate(repos):
        print(f"\t{i + 1} - {n}")
    print()

def listFolders():
    filePath = getDotFilePath()
    repos = parseFileLinesToLists(filePath)
    printRepos(repos)

def RemoveFolder(repo: str):
    filepath = getDotFilePath()
    repos = parseFileLinesToLists(filepath)
    if repo in repos:
        repos.remove(repo)
        dumpStringsListToFile(repos, filepath)
        print(f"\n{repo} Succesfuly removed\n")
    else:
        print(f"\n{repo} is not in the list of repositories")
