import platform, os

class PathNotFoundException(Exception):
    """
    Raised when the path to local chrome cannot be found.
    """

def get_path_macos():
    # ------------------------------ #
    # Uses util mdfind to find the path of Chrome
    # ------------------------------ #

    path = (os.popen("""mdfind \'kMDItemDisplayName == "Google Chrome" && kMDItemKind == Application\'""").read().strip() + "/Contents/MacOS/Google Chrome")
    if len(path) == 0:
        raise PathNotFoundException()

    return path

def get_path_windows():
    # ------------------------------ #
    # Uses util dir to find the path of Chrome
    # ------------------------------ #

    path = (os.popen("""dir "chrome.exe" /s""").read().strip())
    if len(path) == 0:
        raise PathNotFoundException()

    return path

def get_path_linux():
    # ------------------------------ #
    # Uses util which to find the path of Chrome
    # ------------------------------ #
    path = (os.popen("""which google-chrome""").read().strip())
    if len(path) == 0:
        raise PathNotFoundException()

    return path

def get_path():
    if "Darwin" in platform.system():
        return get_path_macos()
    elif "Windows" in platform.system():
        return get_path_windows()
    elif "Linux" in platform.system():
        return get_path_linux()

if __name__ == "__main__":
    print(get_path())
