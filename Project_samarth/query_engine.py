from data_fetch import fetch_crop_data, fetch_rainfall_data
import pandas as pd
import re


# Supported crops and states
crops = ["rice", "wheat", "maize", "sugarcane", "cotton"]
states = [
    "andhra pradesh", "maharashtra", "karnataka", "punjab", "tamil nadu", "bihar",
    "west bengal", "rajasthan", "gujarat", "odisha", "assam", "chhattisgarh",
    "uttar pradesh", "kerala", "telangana", "uttarakhand", "nagaland", "meghalaya",
    "arunachal pradesh", "himachal pradesh", "jammu and kashmir", "tripura",
    "manipur", "jharkhand", "mizoram", "puducherry", "sikkim", "dadra and nagar haveli",
    "goa", "andaman and nicobar islands", "chandigarh"
]


def answer_question(question):
    question_lower = question.lower()
    found_crops = [c for c in crops if c in question_lower]
    found_states = [s for s in states if s in question_lower]


    # ------------------- Crop Production Queries -------------------
    if "production" in question_lower or "most" in question_lower or "highest" in question_lower:
        if not found_crops:
            return "Please specify a crop for production query."
        
        crop = found_crops[0]
        state = found_states[0] if found_states else None


        # Pagination to fetch all records
        limit = 1000
        offset = 0
        all_data = []


        while True:
            df = fetch_crop_data(state=state, crop=crop, limit=limit, offset=offset)
            if df.empty:
                break
            all_data.append(df)
            offset += limit
            
            # Break if we got less than limit (no more data)
            if len(df) < limit:
                break


        if not all_data:
            return f"No production data found for {crop.title()}" + (f" in {state.title()}" if state else "")


        df = pd.concat(all_data, ignore_index=True)


        # State-level → top district
        if state:
            grouped = df.groupby("district_name")["production_"].sum().reset_index()
            top_district = grouped.sort_values("production_", ascending=False).iloc[0]
            return f"Highest {crop.title()} production in {state.title()} is in {top_district['district_name']} ({int(top_district['production_']):,} tons)."


        # National-level → top state
        else:
            grouped = df.groupby("state_name")["production_"].sum().reset_index()
            top_state = grouped.sort_values("production_", ascending=False).iloc[0]
            return f"Highest {crop.title()} production is in {top_state['state_name']} ({int(top_state['production_']):,} tons)."


    # ------------------- Rainfall Queries -------------------
    if "rain" in question_lower or "rainfall" in question_lower:
        if not found_states:
            return "Please specify a state for rainfall data."
        
        state = found_states[0]


        # Extract year if mentioned
        year_match = re.search(r"\b(19|20)\d{2}\b", question_lower)
        year = int(year_match.group()) if year_match else None


        # Pagination to fetch all rainfall records
        limit = 1000
        offset = 0
        all_data = []


        while True:
            df = fetch_rainfall_data(state=state, year=year, limit=limit, offset=offset)
            if df.empty:
                break
            all_data.append(df)
            offset += limit
            
            # Break if we got less than limit (no more data)
            if len(df) < limit:
                break


        if not all_data:
            return f"No rainfall data found for {state.title()}" + (f" in {year}" if year else "")


        df = pd.concat(all_data, ignore_index=True)
        
        # Debug: Print available columns
        print(f"DEBUG: Available columns: {df.columns.tolist()}")
        if not df.empty:
            print(f"DEBUG: First row sample: {df.iloc[0].to_dict()}")


        # Try to find the rainfall column (case-insensitive)
        rainfall_col = None
        for col in df.columns:
            if 'rainfall' in col.lower():
                rainfall_col = col
                break
        
        if not rainfall_col:
            return f"Error: Rainfall column not found. Available columns: {', '.join(df.columns.tolist())}"


        # Convert rainfall to numeric
        df[rainfall_col] = pd.to_numeric(df[rainfall_col], errors="coerce")
        
        # Remove rows with invalid rainfall values
        df = df[df[rainfall_col].notna()]
        
        if df.empty:
            return f"No valid rainfall data found for {state.title()}" + (f" in {year}" if year else "")


        # Try to find year column
        year_col = None
        for col in df.columns:
            if 'year' in col.lower():
                year_col = col
                break
        
        # Filter by year if year was specified and year column exists
        if year and year_col:
            df[year_col] = pd.to_numeric(df[year_col], errors="coerce")
            df_filtered = df[df[year_col] == year]
            
            if df_filtered.empty:
                available_years = sorted(df[year_col].dropna().unique().astype(int).tolist())
                return f"No rainfall data found for {state.title()} in {year}. Available years: {available_years}"
            
            df = df_filtered


        # Calculate average rainfall
        avg_rainfall = df[rainfall_col].mean()
        min_rainfall = df[rainfall_col].min()
        max_rainfall = df[rainfall_col].max()
        
        result = f"Average rainfall in {state.title()}"
        if year:
            result += f" in {year}"
        result += f": {avg_rainfall:.2f} mm"
        
        # Add additional statistics
        total_records = len(df)
        result += f"\n(Min: {min_rainfall:.2f} mm, Max: {max_rainfall:.2f} mm, based on {total_records:,} records)"
        
        return result


    # ------------------- Default fallback -------------------
    return "I can handle rainfall and crop production queries."