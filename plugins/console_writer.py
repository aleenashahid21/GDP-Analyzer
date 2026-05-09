class ConsoleWriter:
    def write(self, data):
        print("\n===== GDP RESULTS =====")

        for k, v in data.items():
            print(f"\n{k.upper()}")

            if k == "top10":
                print("Top 10 Countries by GDP:")
                for item in v:
                    print(f"  {item['Country Name']}: {item['GDP']}")

            elif k == "bottom10":
                print("Bottom 10 Countries by GDP:")
                for item in v:
                    print(f"  {item['Country Name']}: {item['GDP']}")

            elif k == "growth_rate":
                print("GDP Growth Rate of Each Country:")
                for country, rate in v.items():
                    print(f"  {country}: {rate:.2%}")

            elif k == "avg_gdp_continent":
                print("Average GDP by Continent:")
                for cont, avg in v.items():
                    print(f"  {cont}: {avg}")

            elif k == "global_trend":
                print("Total Global GDP Trend:")
                for year, gdp in v.items():
                    print(f"  {year}: {gdp}")

            elif k == "fastest_continent":
                print("Fastest Growing Continent:")
                for cont, rate in v.items():
                    print(f"  {cont}: {rate:.2%}")

            elif k == "decline_countries":
                if v:
                    print("Countries with Consistent GDP Decline:")
                    for country, years in v.items():
                        print(f"  {country}: {years} years")
                else:
                    print("  None found")

            elif k == "continent_contribution":
                print("Contribution of Each Continent to Global GDP:")
                for cont, share in v.items():
                    print(f"  {cont}: {share:.2f}%")

            else:
                # fallback for any other keys
                print(v)
