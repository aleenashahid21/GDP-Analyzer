import matplotlib.pyplot as plt
import os

class ChartWriter:
    def __init__(self, output_dir="charts"):
        os.makedirs(output_dir, exist_ok=True)
        self.output_dir = output_dir

    def write(self, results):
        print("ChartWriter received keys:", results.keys())

        # Top 10 Countries by GDP
        if "top10" in results:
            countries = [item["Country Name"] for item in results["top10"]]
            gdps = [item["GDP"] for item in results["top10"]]
            plt.figure(figsize=(12,8))
            plt.barh(countries, gdps)
            plt.title("Top 10 Countries by GDP")
            plt.xlabel("GDP")
            plt.ylabel("Country")
            plt.tight_layout()
            plt.savefig(os.path.join(self.output_dir, "top10.png"))
            plt.close()

        # Bottom 10 Countries by GDP
        if "bottom10" in results:
            countries = [item["Country Name"] for item in results["bottom10"]]
            gdps = [item["GDP"] for item in results["bottom10"]]
            plt.figure(figsize=(12,8))
            plt.barh(countries, gdps, color="orange")
            plt.title("Bottom 10 Countries by GDP")
            plt.xlabel("GDP")
            plt.ylabel("Country")
            plt.tight_layout()
            plt.savefig(os.path.join(self.output_dir, "bottom10.png"))
            plt.close()

        # GDP Growth Rate of Each Country
        if "growth_rate" in results:
            countries = list(results["growth_rate"].keys())
            growth = list(results["growth_rate"].values())
            plt.figure(figsize=(14,8))
            plt.barh(countries, growth, color="skyblue")
            plt.title("GDP Growth Rate of Each Country")
            plt.xlabel("Growth Rate (%)")
            plt.ylabel("Country")
            plt.tight_layout()
            plt.savefig(os.path.join(self.output_dir, "growth_rate.png"))
            plt.close()

        # Average GDP by Continent
        if "avg_gdp_continent" in results:
            continents = list(results["avg_gdp_continent"].keys())
            avg_gdp = list(results["avg_gdp_continent"].values())
            plt.figure(figsize=(10,6))
            plt.bar(continents, avg_gdp)
            plt.title("Average GDP by Continent")
            plt.xlabel("Continent")
            plt.ylabel("Average GDP")
            plt.tight_layout()
            plt.savefig(os.path.join(self.output_dir, "avg_gdp_continent.png"))
            plt.close()

        # Global GDP Trend
        if "global_trend" in results:
            years = list(results["global_trend"].keys())
            gdp_values = list(results["global_trend"].values())
            plt.figure(figsize=(10,6))
            plt.plot(years, gdp_values, marker="o")
            plt.title("Total Global GDP Trend")
            plt.xlabel("Year")
            plt.ylabel("GDP")
            plt.grid(True)
            plt.tight_layout()
            plt.savefig(os.path.join(self.output_dir, "global_trend.png"))
            plt.close()

        # Fastest Growing Continent
        if "fastest_continent" in results:
            continents = list(results["fastest_continent"].keys())
            growth = list(results["fastest_continent"].values())
            plt.figure(figsize=(10,6))
            plt.bar(continents, growth, color="green")
            plt.title("Fastest Growing Continent")
            plt.xlabel("Continent")
            plt.ylabel("Growth Rate (%)")
            plt.tight_layout()
            plt.savefig(os.path.join(self.output_dir, "fastest_continent.png"))
            plt.close()

        # Countries with Consistent GDP Decline
        if "decline_countries" in results and results["decline_countries"]:
            countries = list(results["decline_countries"].keys())
            decline_years = list(results["decline_countries"].values())
            plt.figure(figsize=(12,8))
            plt.barh(countries, decline_years, color="red")
            plt.title("Countries with Consistent GDP Decline")
            plt.xlabel("Years of Decline")
            plt.ylabel("Country")
            plt.tight_layout()
            plt.savefig(os.path.join(self.output_dir, "decline_countries.png"))
            plt.close()

        # Contribution of Each Continent to Global GDP
        if "continent_contribution" in results:
            continents = list(results["continent_contribution"].keys())
            contributions = list(results["continent_contribution"].values())
            plt.figure(figsize=(8,8))
            plt.pie(contributions, labels=continents, autopct="%1.1f%%")
            plt.title("Contribution of Each Continent to Global GDP")
            plt.tight_layout()
            plt.savefig(os.path.join(self.output_dir, "continent_contribution.png"))
            plt.close()
