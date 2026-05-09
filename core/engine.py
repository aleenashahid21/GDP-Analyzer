import pandas as pd
from core.contracts import DataSink, PipelineService

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
        start_year = self.config.get("start_year", melted["Year"].min())
        end_year = self.config.get("end_year", melted["Year"].max())
        decline_years = self.config.get("decline_years", 5)

        # Subset for given continent & year
        subset = melted[
            (melted["Continent"] == continent) &
            (melted["Year"] == year)
        ]

        # Top & Bottom 10
        results["top10"] = subset.sort_values("GDP", ascending=False).head(10).to_dict("records")
        results["bottom10"] = subset.sort_values("GDP").head(10).to_dict("records")

        # Global GDP Trend
        trend = melted.groupby("Year")["GDP"].sum()
        results["global_trend"] = trend.to_dict()

        # GDP Growth Rate of Each Country (within continent, across range)
        growth = (
            melted[(melted["Continent"] == continent) & (melted["Year"].between(start_year, end_year))]
            .groupby("Country Name")["GDP"]
            .pct_change()
            .groupby(melted["Country Name"])
            .mean()
        )
        results["growth_rate"] = growth.dropna().to_dict()

        # Average GDP by Continent (date range)
        avg_gdp = melted[melted["Year"].between(start_year, end_year)].groupby("Continent")["GDP"].mean()
        results["avg_gdp_continent"] = avg_gdp.to_dict()

        # Fastest Growing Continent
        continent_growth = (
            melted[melted["Year"].between(start_year, end_year)]
            .groupby(["Continent","Year"])["GDP"].sum()
            .groupby("Continent")
            .pct_change()
            .groupby("Continent")
            .mean()
        )
        results["fastest_continent"] = continent_growth.dropna().to_dict()

        # Countries with Consistent GDP Decline (last x years)
        decline = {}
        for country, group in melted.groupby("Country Name"):
            last_years = group.sort_values("Year").tail(decline_years)
            if all(last_years["GDP"].diff().dropna() < 0):
                decline[country] = decline_years
        results["decline_countries"] = decline

        # Contribution of Each Continent to Global GDP (date range)
        contribution = melted[melted["Year"].between(start_year, end_year)].groupby("Continent")["GDP"].sum()
        total = contribution.sum()
        results["continent_contribution"] = (contribution / total * 100).to_dict()

        self.sink.write(results)
