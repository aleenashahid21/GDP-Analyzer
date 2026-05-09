import pandas as pd
import os

class DataReader:   # you might rename this to DataReader since it’s no longer just CSV
    def __init__(self, service, path):
        self.service = service
        self.path = path

    def run(self):
        # detect file extension
        ext = os.path.splitext(self.path)[1].lower()

        if ext == ".csv":
            df = pd.read_csv(self.path)
        elif ext in [".xlsx", ".xls"]:
            df = pd.read_excel(self.path)
        elif ext == ".json":
            df = pd.read_json(self.path)
        else:
            raise ValueError(f"Unsupported file type: {ext}")

        self.service.execute(df)
