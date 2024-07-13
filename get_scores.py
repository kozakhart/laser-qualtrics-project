import csv
import pandas as pd
from datetime import datetime

net_id= 'Q6...296'
first_name = "RecipientFirstName"
last_name = "RecipientLastName"
to_date= "CurrentDate"
from_date= "two years earlier"
language_abbre = "Q4_1...199"
backup_language_abbre = "Q10...279"
#all_data.csv
byu_id = "Q5...97"

#score sheet
byu_id_2 = "candidateid"
first_name_2 = "Candidate First Name"
last_name_2 = "Candidate Last Name"
language_2 = "Language"
test_date = "Test Date"
rating = "Rating"



df1 = pd.read_csv('your_output_file.csv')
df2 = pd.read_csv('WPT.csv')

# Iterate over the rows of df1
counter = 0
for index, row in df1.iterrows():
    if index == 0:
        continue
    byu_id = row['Q5...97']
    # Find the matching row in df2
    matching_row = df2[df2['candidateid'] == byu_id]
    
    if not matching_row.empty:
        # Get the Rating value
        rating = matching_row.iloc[0]['Rating']
        date = matching_row.iloc[0]['Test Date']
        # Update the OPI_Score in df1
        df1.at[index, 'WPT_Score'] = rating
        df1.at[index, 'WPT_Date'] = date

    else:
        counter += 1

print("Scores not found =", counter)

# Save the updated DataFrame back to a CSV file
df1.to_csv('updated_sheet1.csv', index=False)


# df = pd.read_csv('all_data.csv', encoding='utf-8')

# # Save the DataFrame to a CSV file with utf-8-sig encoding
# df.to_csv('your_output_file.csv', index=False, encoding='utf-8-sig')