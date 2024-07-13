import pandas as pd
from datetime import datetime
# Define the score to numeric value mappings
ratings_map = {
    "S": "10",
    "AH": "9",
    "AM": "8",
    "AL": "7",
    "IH": "6",
    "IM": "5",
    "IL": "4",
    "NH": "3",
    "NM": "2",
    "NL": "1",
    "": "0"  # Assuming empty string maps to 0 or some other numeric value
}

# Load the CSV file into a DataFrame
df1 = pd.read_csv('query-results(48).csv')

# Iterate over the rows of df1

self_speak = "SelfAssessSpeak_Ave"
self_write = "SelfAssessWrite_Ave"

for index, row in df1.iterrows():

    
    # Replace the scores with numeric values
    df1.at[index, 'OPIc_Score'] = ratings_map.get(row['OPIc_Score'], row['OPIc_Score'])
    df1.at[index, 'OPI_Score'] = ratings_map.get(row['OPI_Score'], row['OPI_Score'])
    df1.at[index, 'WPT_Score'] = ratings_map.get(row['WPT_Score'], row['WPT_Score'])

    try:
        df1.at[index, "Writing_Calibration_Score"] = float(row[self_write]) - float(ratings_map.get(row['WPT_Score'], row['WPT_Score'])) 
    except:
        df1.at[index, "Writing_Calibration_Score"] = "NA"


    # opic_score = row['OPIc_Score']
    # opi_score = row['OPI_Score']
    recorded_date_str = row['RecordedDate']
    opic_date_str = row['OPIc_Date']
    opi_date_str = row['OPI_Date']

    recorded_date = datetime.strptime(recorded_date_str, "%m/%d/%Y") if pd.notna(recorded_date_str) else None
    opic_date = datetime.strptime(opic_date_str, "%m/%d/%Y") if pd.notna(opic_date_str) else None
    opi_date = datetime.strptime(opi_date_str, "%m/%d/%Y") if pd.notna(opi_date_str) else None

    try:

        if pd.notna(opic_date_str) and pd.notna(opi_date_str):
            diff1 = abs((recorded_date - opic_date).days)
            diff2 = abs((recorded_date - opi_date).days)
            if diff1 < diff2:
                closest_score = row['OPIc_Score']
            else:
                closest_score = row['OPI_Score']

            df1.at[index, "Speaking_Calibration_Score"] = float(row[self_speak]) - float(ratings_map.get(closest_score, closest_score))

        elif pd.notna(opic_date_str):
            df1.at[index, "Speaking_Calibration_Score"] = float(row[self_speak]) - float(ratings_map.get(row['OPIc_Score'], row['OPIc_Score']))
        elif pd.notna(opi_date_str):
            df1.at[index, "Speaking_Calibration_Score"] = float(row[self_speak]) - float(ratings_map.get(row['OPI_Score'], row['OPI_Score']))
        else:
          df1.at[index, "Speaking_Calibration_Score"] = "NA"  
    except:
        df1.at[index, "Speaking_Calibration_Score"] = "NA"

    
df1.to_csv('query-results-updated.csv', index=False, encoding='utf-8-sig')

# Display the updated DataFrame to verify the changes
print(df1.head())



