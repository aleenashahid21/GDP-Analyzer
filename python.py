import pandas as pd
import json

# =========================
# CONTRACTS (Protocols)
# =========================
from typing import Protocol, runtime_checkable, Any

@runtime_checkable
class DataSink(Protocol):
    def write(self, data: dict) -> None:
        ...

@runtime_checkable
class PipelineService(Protocol):
    def execute(self, raw_data: Any) -> None:
        ...

# =========================
# CORE ENGINE
# =========================
class TransformationEngine(PipelineService):
    def __init__(self, sink: DataSink, config: dict):
        self.sink = sink
        self.config = config

    def execute(self, raw_data):
        df = raw_data
        year_cols = [c for c in df.columns if str(c).isdigit()]

        melted = df.melt(
            id_vars=["Country Name", "Continent"],
            value_vars=year_cols,
            var_name="Year",
            value_name="GDP"
        )

        melted["Year"] = melted["Year"].astype(int)
        melted = melted.dropna()

        results = {}
        year = self.config["year"]
        continent = self.config["continent"]

        subset = melted[
            (melted["Continent"] == continent) &
            (melted["Year"] == year)
        ]

        results["top10"] = subset.sort_values("GDP", ascending=False).head(10).to_dict("records")
        results["bottom10"] = subset.sort_values("GDP").head(10).to_dict("records")

        trend = melted.groupby("Year")["GDP"].sum()
        results["global_trend"] = trend.to_dict()

        self.sink.write(results)

# =========================
# INPUT PLUGIN (CSV Reader)
# =========================
class CSVReader:
    def __init__(self, service, path):
        self.service = service
        self.path = path

    def run(self):
        df = pd.read_csv(self.path)
        self.service.execute(df)

# =========================
# OUTPUT PLUGIN (Console Writer)
# =========================
class ConsoleWriter:
    def write(self, data):
        print("\n===== GDP RESULTS =====")
        for k, v in data.items():
            print(f"\n{k.upper()}")
            print(v)

# =========================
# MAIN ORCHESTRATOR
# =========================
INPUT_DRIVERS = {
    "csv": CSVReader
}

OUTPUT_DRIVERS = {
    "console": ConsoleWriter
}

def load_config():
    with open("config.json") as f:
        return json.load(f)

def bootstrap():
    config = load_config()
    sink = OUTPUT_DRIVERS[config["output"]]()
    engine = TransformationEngine(sink, config)
    reader = INPUT_DRIVERS[config["input"]](engine, config["data_path"])
    reader.run()

# =========================
# SAMPLE CONFIG + DATA
# =========================
def setup_sample():
    # Create config.json
    config = {
        "input": "csv",
        "output": "console",
        "data_path": "sample_gdp.csv",
        "continent": "Asia",
        "year": 2020
    }
    with open("config.json", "w") as f:
        json.dump(config, f, indent=4)

    # Create sample CSV
    data = {
        "Country Name": ["Pakistan", "India", "China", "Germany", "France"],
        "Continent": ["Asia", "Asia", "Asia", "Europe", "Europe"],
        "2018": [314, 2700, 13600, 4000, 2800],
        "2019": [278, 2900, 14300, 4100, 2900],
        "2020": [263, 2700, 14700, 3800, 2700],
    }
    df = pd.DataFrame(data)
    df.to_csv("sample_gdp.csv", index=False)

# =========================
# RUN PROJECT
# =========================
if __name__ == "__main__":
    setup_sample()
    print("Project setup complete. Running...\n")
    bootstrap()
