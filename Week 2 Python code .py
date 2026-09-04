Appendix A. Python Code
import pandas as pd
import matplotlib.pyplot as plt
 
# Main COVID-19 reported cases/deaths data
df = pd.read_csv("WHO-COVID-19-global-data.csv")
df["Date_reported"] = pd.to_datetime(df["Date_reported"], errors="coerce")
 
# Global time series
global_week = (
    df.groupby("Date_reported")[["New_cases", "New_deaths"]]
      .sum(min_count=1)
      .reset_index()
)
 
# Selected-country rolling case comparison
countries = [
    "India",
    "United States of America",
    "Brazil",
    "United Kingdom of Great Britain and Northern Ireland",
    "Germany"
]
 
for country in countries:
    sub = df[df["Country"] == country].sort_values("Date_reported").copy()
    sub["rolling"] = (
        sub["New_cases"].fillna(0)
        .rolling(4, min_periods=1)
        .mean()
    )
    plt.plot(sub["Date_reported"], sub["rolling"], label=country)
 
plt.title("COVID-19 Waves Across Five Major Countries")
plt.xlabel("Date")
plt.ylabel("Reported new cases (4-week rolling average)")
plt.legend()
plt.tight_layout()
plt.savefig("02_country_waves.png", dpi=180)
plt.close()
 
# Vaccination
vax = pd.read_csv("COV_VAC_UPTAKE_2021_2023.csv")
vax["DATE"] = pd.to_datetime(vax["DATE"], errors="coerce")
 
# Age-specific deaths
age = pd.read_csv("WHO-COVID-19-global-monthly-death-by-age-data.csv")
age["Deaths"] = pd.to_numeric(age["Deaths"], errors="coerce")
age_total = age.groupby("Agegroup")["Deaths"].sum()
 
# Mortality ranking
table = pd.read_csv("WHO-COVID-19-global-table-data.csv")
table["Cases - cumulative total"] = pd.to_numeric(
    table["Cases - cumulative total"], errors="coerce"
)
table["Deaths - cumulative total per 100000 population"] = pd.to_numeric(
    table["Deaths - cumulative total per 100000 population"],
    errors="coerce"
)
 
mortality = table[
    (table["Name"] != "Global") &
    (table["Cases - cumulative total"] >= 100000)
].sort_values(
    "Deaths - cumulative total per 100000 population",
    ascending=False
).head(10)
 
# Hospitalization
hosp = pd.read_csv("WHO-COVID-19-global-hosp-icu-data.csv")
hosp["Date_reported"] = pd.to_datetime(hosp["Date_reported"], errors="coerce")
