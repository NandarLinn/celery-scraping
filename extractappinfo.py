from androguard.core.bytecodes.apk import APK

class APKAnalyzer:
    """
    A class to analyze APK files and extract metadata like package name,
    version, and permissions.
    """
    def __init__(self, apk_file_path):
        """
        Initialize the APKAnalyzer with the path to the APK file.
        """
        self.apk_file_path = apk_file_path
        self.apk = None

    def load_apk(self):
        """
        Load and parse the APK file.
        """
        try:
            self.apk = APK(self.apk_file_path)
        except Exception as e:
            raise ValueError(f"Failed to load APK file: {e}")

    def get_package_name(self):
        """
        Get the package name of the APK.
        """
        if self.apk:
            return self.apk.package
        return None

    def get_version_info(self):
        """
        Get the version code and version name of the APK.
        """
        if self.apk:
            return {
                "version_code": self.apk.get_androidversion_code(),
                "version_name": self.apk.get_androidversion_name()
            }
        return None

    def get_permissions(self):
        """
        Get the list of permissions requested by the APK.
        """
        if self.apk:
            return self.apk.get_permissions()
        return None

    def analyze(self):
        """
        Perform a full analysis of the APK and return key metadata.
        """
        if not self.apk:
            self.load_apk()

        return {
            "package_name": self.get_package_name(),
            "version_info": self.get_version_info(),
            "permissions": self.get_permissions()
        }


# Example Usage
if __name__ == "__main__":
    apk_path = "insta.apk"  # Replace with your APK file path
    analyzer = APKAnalyzer(apk_path)

    try:
        metadata = analyzer.analyze()
        print("APK Metadata:")
        print(f"Package Name: {metadata['package_name']}")
        print(f"Version Info: {metadata['version_info']}")
        print(f"Permissions: {', '.join(metadata['permissions'])}")
    except ValueError as e:
        print(f"Error: {e}")
