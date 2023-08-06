import pkg_resources

try:
    __version__ = pkg_resources.get_distribution("AlekSIS-App-CSVImport").version
except Exception:
    __version__ = "unknown"

default_app_config = "aleksis.apps.csv_import.apps.CSVImportConfig"
