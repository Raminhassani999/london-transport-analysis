
import pandas as pd
from pathlib import Path



raw_file = Path("data/raw/tfl-journeys-type.csv")
df = pd.read_csv(raw_file)


df["Period beginning"] = pd.to_datetime(
    df["Period beginning"], format="%d-%b-%y", errors="raise"
)

df["Period ending"] = pd.to_datetime(
    df["Period ending"], format="%d-%b-%y", errors="raise"
)


df = df.rename(columns={
    "Period and Financial year": "period_and_financial_year",
    "Reporting Period": "reporting_period",
    "Days in period": "days_in_period",
    "Period beginning": "period_beginning",
    "Period ending": "period_ending",
    "Bus journeys (m)": "bus_journeys_m",
    "Underground journeys (m)": "underground_journeys_m",
    "DLR Journeys (m)": "dlr_journeys_m",
    "Tram Journeys (m)": "tram_journeys_m",
    "Overground Journeys (m)": "overground_journeys_m",
    "London Cable Car Journeys (m)": "london_cable_car_journeys_m",
    "TfL Rail Journeys (m)": "tfl_rail_journeys_m",
})


print("Dataset shape:", df.shape)
print("\nColumn names:")
print(df.columns.tolist())

print("\nData types:")
print(df.dtypes)

print("\nFirst five rows:")
print(df.head())


print("\nMissing values:")
print(df.isna().sum())

print("\nMissing values (%):")
print((df.isna().mean() * 100).round(2))


print("\nDuplicate rows:", df.duplicated().sum())



print("\nFirst period beginning:", df["period_beginning"].min())
print("Last period ending:", df["period_ending"].max())

print(
    "\nBeginning dates sorted:",
    df["period_beginning"].is_monotonic_increasing,
)

print(
    "\nPeriods ending before they begin:",
    (df["period_ending"] < df["period_beginning"]).sum(),
)



df["expected_financial_year"] = df["period_beginning"].apply(
    lambda date: (
        f"{str(date.year)[-2:]}/{str(date.year + 1)[-2:]}"
        if date.month >= 4
        else f"{str(date.year - 1)[-2:]}/{str(date.year)[-2:]}"
    )
)

df["label_financial_year"] = df["period_and_financial_year"].str[-5:]

df["financial_year_matches"] = (
    df["expected_financial_year"] == df["label_financial_year"]
)

print("\nFinancial-year label mismatches:")
print(
    df.loc[
        ~df["financial_year_matches"],
        [
            "period_and_financial_year",
            "period_beginning",
            "expected_financial_year",
            "label_financial_year",
        ],
    ]
)



df["period_and_financial_year"] = df.apply(
    lambda row: (
        f"{row['reporting_period']:02d}_"
        f"{str(row['period_beginning'].year)[-2:]}/"
        f"{str(row['period_beginning'].year + 1)[-2:]}"
        if row["period_beginning"].month >= 4
        else f"{row['reporting_period']:02d}_"
        f"{str(row['period_beginning'].year - 1)[-2:]}/"
        f"{str(row['period_beginning'].year)[-2:]}"
    ),
    axis=1,
)



df["label_financial_year"] = df["period_and_financial_year"].str[-5:]

df["financial_year_matches"] = (
    df["expected_financial_year"] == df["label_financial_year"]
)

print("\nFinancial-year mismatches after correction:")
print((~df["financial_year_matches"]).sum())

print(
    "Duplicate financial-period labels:",
    df["period_and_financial_year"].duplicated().sum(),
)

df["calculated_days"] = (
    df["period_ending"] - df["period_beginning"]
).dt.days + 1

mismatches = df["days_in_period"] != df["calculated_days"]

print("\nDay-count mismatches:", mismatches.sum())

print(
    df.loc[
        mismatches,
        [
            "period_and_financial_year",
            "period_beginning",
            "period_ending",
            "days_in_period",
            "calculated_days",
        ],
    ]
)
