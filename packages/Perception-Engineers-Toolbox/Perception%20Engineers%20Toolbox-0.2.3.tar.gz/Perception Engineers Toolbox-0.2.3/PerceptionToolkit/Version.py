class Version:
    """
    Represents a version number.
    """
    major: int
    minor: int
    release: int

    def __init__(self, major: int = 0, minor: int = 0, release: int = 0):
        self.major = major
        self.minor = minor
        self.release = release

    def __bool__(self) -> bool:
        return not(self.major == 0 and self.minor == 0 and self.release == 0)

    def __eq__(self, other) -> bool:
        """Check whether two versions are equal"""
        return self.major == other.major and self.minor == other.minor and self.release == other.release

    def __ge__(self, other) -> bool:
        """check whether the version is equal or newer than"""
        if self.major < other.major:
            return False
        if self.major == other.major:
            if self.minor < other.minor:
                return False
            if self.minor == other.minor:
                if self.release < other.release:
                    return False
                if self.release == other.release:
                    return True
        return True

    def __str__(self) -> str:
        return "%i.%i.%i" % (self.major, self.minor, self.release)

    @staticmethod
    def from_str(string: str):
        parts = string.split(".")
        assert (len(parts) == 3)
        return Version(int(parts[0]), int(parts[1]), int(parts[2]))


# The core library version
__version__: Version = Version(0, 2, 3)
version_str: str = str(__version__)
