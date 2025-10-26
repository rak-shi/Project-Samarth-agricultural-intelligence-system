import requests
import pandas as pd
import re

API_KEY = "579b464db66ec23bdd00000161c8d205d2e3411c6aa6d4cd829f40f6"
CROP_RESOURCE_ID = "35be999b-0208-4354-b557-f6ca9a5355de"
RAINFALL_RESOURCE_ID = "6c05cd1b-ed59-40c2-bc31-e314f39c6971"

crops = ["rice", "wheat", "maize", "sugarcane", "cotton"]
states = [
    "andhra pradesh", "maharashtra", "karnataka", "punjab", "tamil nadu", "bihar",
    "west bengal", "rajasthan", "gujarat", "odisha", "assam", "chhattisgarh",
    "uttar pradesh", "kerala", "telangana", "uttarakhand", "nagaland", "meghalaya",
    "arunachal pradesh", "himachal pradesh", "jammu and kashmir", "tripura",
    "manipur", "jharkhand", "mizoram", "puducherry", "sikkim",
    "dadra and nagar haveli", "goa", "andaman and nicobar islands", "chandigarh"
]

def fetch_crop_data(state=None, crop=None, year=None, season=None, limit=1000, offset=0):
    if state:
        state = state.title()
    if crop:
        crop = crop.title()

    url = f"https://api.data.gov.in/resource/{CROP_RESOURCE_ID}?api-key={API_KEY}&format=json&limit={limit}&offset={offset}"
    if state:
        url += f"&filters[state_name]={state}"
    if crop:
        url += f"&filters[crop]={crop}"
    if year:
        url += f"&filters[crop_year]={year}"
    if season:
        url += f"&filters[season]={season}"

    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            print(f"Error fetching crop data: {response.status_code}")
            return pd.DataFrame()

        data = response.json().get("records", [])
        df = pd.DataFrame(data)
        if df.empty:
            return df

        df.columns = df.columns.str.lower()
        for col in ["production_", "area_", "crop_year"]:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce")
        return df
    except Exception as e:
        print(f"Exception fetching crop data: {e}")
        return pd.DataFrame()

def fetch_rainfall_data(state, year=None, limit=1000, offset=0):
    if state:
        state = state.title()

    url = f"https://api.data.gov.in/resource/{RAINFALL_RESOURCE_ID}?api-key={API_KEY}&format=json&limit={limit}&offset={offset}"
    url += f"&filters[State]={state}"
    if year:
        url += f"&filters[Year]={year}"

    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            print(f"Error fetching rainfall data: {response.status_code}")
            return pd.DataFrame()

        data = response.json().get("records", [])
        df = pd.DataFrame(data)
        if df.empty:
            return df

        df.columns = df.columns.str.lower()
        if "year" in df.columns:  # Ensure year is numeric
            df["year"] = pd.to_numeric(df["year"], errors="coerce")
        if "avg_rainfall" in df.columns:
            df["avg_rainfall"] = pd.to_numeric(df["avg_rainfall"], errors="coerce")
        df = df[df["avg_rainfall"].notna()]
        return df
    except Exception as e:
        print(f"Exception fetching rainfall data: {e}")
        return pd.DataFrame()

def get_latest_year(df, year_col):
    """Get most recent year available in DataFrame"""
    if year_col in df.columns and not df.empty:
        years = df[year_col].dropna().unique()
        return int(max(years)) if len(years) > 0 else None
    return None

def answer_question(question):
    question_lower = question.lower()
    found_crops = [c for c in crops if c in question_lower]
    found_states = [s for s in states if s in question_lower]

    # --------------- Production Queries (with citation/year) ---------------
    if any(keyword in question_lower for keyword in ["production", "most", "highest", "yield"]):
        if not found_crops:
            return "Please specify a crop for production query."

        crop = found_crops[0]
        state = found_states[0] if found_states else None

        all_data, limit, offset = [], 1000, 0
        while True:
            df = fetch_crop_data(state=state, crop=crop, limit=limit, offset=offset)
            if df.empty:
                break
            all_data.append(df)
            offset += limit
            if len(df) < limit:
                break

        if not all_data or all([d.empty for d in all_data]):
            return f"No production data found for {crop.title()}" + (f" in {state.title()}" if state else "") + f"\nSource: data.gov.in [{CROP_RESOURCE_ID}]"

        df = pd.concat(all_data, ignore_index=True)
        # Use most recent year
        year_col = "crop_year"
        latest_year = get_latest_year(df, year_col)

        # Filter by most recent year (if available)
        if latest_year:
            df = df[df["crop_year"] == latest_year]

        if state:
            grouped = df.groupby("district_name")["production_"].sum().reset_index()
            top = grouped.sort_values("production_", ascending=False).iloc[0]
            result = f"Highest {crop.title()} production in {state.title()} (year {latest_year}) is in {top['district_name']} ({int(top['production_']):,} tons)."
        else:
            grouped = df.groupby("state_name")["production_"].sum().reset_index()
            top = grouped.sort_values("production_", ascending=False).iloc[0]
            result = f"Highest {crop.title()} production in India (year {latest_year}) is in {top['state_name']} ({int(top['production_']):,} tons)."
        result += f"\nSource: data.gov.in [{CROP_RESOURCE_ID}]"
        return result

    # --------------- Rainfall Queries ---------------
    if "rain" in question_lower or "rainfall" in question_lower:
        if not found_states:
            return "Please specify a state for rainfall data."

        state = found_states[0]
        year_match = re.search(r"\b(19|20)\d{2}\b", question_lower)
        year = int(year_match.group()) if year_match else None

        all_data, limit, offset = [], 1000, 0
        while True:
            df = fetch_rainfall_data(state=state, year=year, limit=limit, offset=offset)
            if df.empty:
                break
            all_data.append(df)
            offset += limit
            if len(df) < limit:
                break

        if not all_data or all([d.empty for d in all_data]):
            return f"No rainfall data found for {state.title()}" + (f" in {year}" if year else "") + f"\nSource: data.gov.in [{RAINFALL_RESOURCE_ID}]"

        df = pd.concat(all_data, ignore_index=True)
        year_col = "year"
        rainfall_col = "avg_rainfall"
        # If year not given, use latest year
        used_year = year if year else get_latest_year(df, year_col)
        if used_year:
            df = df[df[year_col] == used_year]

        df[rainfall_col] = pd.to_numeric(df[rainfall_col], errors="coerce")
        df = df[df[rainfall_col].notna()]

        avg_rainfall = df[rainfall_col].mean()
        min_rainfall = df[rainfall_col].min()
        max_rainfall = df[rainfall_col].max()
        total_records = len(df)

        result = f"Average rainfall in {state.title()}"
        if used_year:
            result += f" in {used_year}"
        result += f": {avg_rainfall:.2f} mm"
        result += f"\n(Min: {min_rainfall:.2f} mm, Max: {max_rainfall:.2f} mm, based on {total_records:,} records)"
        result += f"\nSource: data.gov.in [{RAINFALL_RESOURCE_ID}]"
        return result

    # --------------- Default / Help Output ---------------
    return (
        "I can answer queries about crop production and rainfall in India. "
        "Answers are sourced live from government datasets and include citations for traceability."
        "\nSource (crop): data.gov.in [{}]\nSource (rainfall): data.gov.in [{}]".format(CROP_RESOURCE_ID, RAINFALL_RESOURCE_ID)
    )
