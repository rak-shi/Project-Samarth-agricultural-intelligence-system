import requests
import pandas as pd


API_KEY = "579b464db66ec23bdd00000150781e6287b8491b4a1fb14a0352c4e4"


# Resource IDs
CROP_RESOURCE_ID = "35be999b-0208-4354-b557-f6ca9a5355de"
RAINFALL_RESOURCE_ID = "6c05cd1b-ed59-40c2-bc31-e314f39c6971"


# ---------------- Crop Data -----------------
def fetch_crop_data(state=None, crop=None, year=None, season=None, limit=1000, offset=0):
    """
    Fetch district-wise crop production data from data.gov.in API.
    Returns a DataFrame.
    """
    if crop:
        crop = crop.title()
    if state:
        state = state.title()


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


        # Convert numeric columns
        if "production_" in df.columns:
            df["production_"] = pd.to_numeric(df["production_"], errors="coerce")
        if "area_" in df.columns:
            df["area_"] = pd.to_numeric(df["area_"], errors="coerce")


        df.columns = df.columns.str.lower()
        return df
    
    except Exception as e:
        print(f"Exception fetching crop data: {e}")
        return pd.DataFrame()


# ---------------- Rainfall Data -----------------
def fetch_rainfall_data(state, year=None, limit=1000, offset=0):
    """
    Fetch daily district-wise rainfall data for a given state from data.gov.in
    Returns a DataFrame.
    """
    if state:
        state = state.title()


    url = f"https://api.data.gov.in/resource/{RAINFALL_RESOURCE_ID}?api-key={API_KEY}&format=json&limit={limit}&offset={offset}"
    if state:
        url += f"&filters[State]={state}"
    if year:
        url += f"&filters[Year]={year}"


    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            print(f"Error fetching rainfall data: {response.status_code}")
            print(f"Response: {response.text[:200]}")
            return pd.DataFrame()


        data = response.json().get("records", [])
        
        # Debug: print response structure
        if data:
            print(f"DEBUG: Sample record keys: {data[0].keys()}")
        
        df = pd.DataFrame(data)
        if df.empty:
            return df


        # Print original column names before lowercasing
        print(f"DEBUG: Original columns: {df.columns.tolist()}")
        
        # Convert to lowercase for consistency
        df.columns = df.columns.str.lower()
        
        # Convert numeric columns - try different possible rainfall column names
        for col in df.columns:
            if 'rainfall' in col.lower():
                df[col] = pd.to_numeric(df[col], errors="coerce")
                print(f"DEBUG: Found and converted rainfall column: {col}")
        
        # Convert year column if it exists
        for col in df.columns:
            if 'year' in col.lower():
                df[col] = pd.to_numeric(df[col], errors="coerce")
                print(f"DEBUG: Found and converted year column: {col}")

        return df
    
    except Exception as e:
        print(f"Exception fetching rainfall data: {e}")
        return pd.DataFrame()