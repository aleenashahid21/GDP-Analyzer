import sys, os, json

sys.path.append(os.getcwd())

from core.engine import TransformationEngine
from plugins.DataReader import DataReader
from plugins.console_writer import ConsoleWriter
from plugins.chart_writer import ChartWriter


INPUT_DRIVERS = {
    "data": DataReader
}

OUTPUT_DRIVERS = {
    "console": ConsoleWriter,
    "chart": ChartWriter
}


def load_config():

    with open("config.json") as f:
        return json.load(f)


def bootstrap():

    config = load_config()

    sink = OUTPUT_DRIVERS[config["output"]]()

    engine = TransformationEngine(sink, config)

    reader = INPUT_DRIVERS[config["input"]](
        engine,
        config["data_path"]
    )

    reader.run()


if __name__ == "__main__":
    bootstrap()
