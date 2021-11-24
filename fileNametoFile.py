import os

def parseFoldertoFindWidgets(folder):
    assert folder is not None
    with open("outputfile.txt", "w") as f:
        for subdir, dirs, files in os.walk(folder):
            for filename in files:
                if filename.__contains__("Widget_v3") and not filename.__contains__(".meta"):
                    f.write(filename + "\n")

parseFoldertoFindWidgets(r"/Users/joshsallows/2020_project/Assets/Prefabs/UI_v3 prefabs/widgets/")