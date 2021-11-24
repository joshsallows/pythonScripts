import os

def parseFoldersToRenameFiles(folder):
    assert folder is not None
    for subdir, dirs, files in os.walk(folder):
        for filename in files:
            filepath = subdir + os.sep + filename
            if filepath.endswith(".dsav"):
                 print(filename)
parseFolderforSimSaveState()