import os


class Renamer:
    def __init__(self, path):
        os.chdir(path)

    @classmethod
    def getwd(cls):
        return cls(input("Enter path to the directory: "))

    def rename(self, series_list):
        path = os.getcwd()
        dir_list = next(os.walk("."))[2]
        if dir_list:
            for src, dst in zip(dir_list, series_list):
                ext = os.path.splitext(src)[1]
                os.rename(
                    os.path.join(path, src), os.path.join(path, "".join([dst, ext]))
                )
            print("Done!")
        else:
            print("Directory", path, "is empty.")
