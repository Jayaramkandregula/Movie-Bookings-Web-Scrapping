from bs4 import BeautifulSoup
import pandas as pd
import os
from datetime import datetime

columns = [
    'Theatre Name',
    'Date',
    'Time',
    'Total Tickets',
    'Total Booked Tickets',
    'Total Available Tickets',
    'Total Tickets Cost',
    'Total Booked Tickets Cost',
    'Total Available Tickets Cost',
    'Updated Time'
]
def check_or_create_movie_stats_csv(file_path, columns):
    if not os.path.isfile(file_path) or os.stat(file_path).st_size == 0:
        # Create a new DataFrame with the specified headers
        df = pd.DataFrame(columns=columns)
        # Save it to the CSV file
        df.to_csv(file_path, index=False)
        print(f"Created new CSV file with headers: {columns}")
    else:
        # Load the existing DataFrame
        df = pd.read_csv(file_path)
        print("Loaded existing CSV file.")
    return df


def update_movie_stats_csv(file_path, new_data):
    # Check if the CSV file exists and create it if necessary
    df = check_or_create_movie_stats_csv(file_path, columns)

    # Convert the list of new data into a DataFrame
    new_df = pd.DataFrame(new_data, columns=columns)

    # Merge the new data with the existing DataFrame
    df = pd.concat([df, new_df], ignore_index=True)

    # Drop duplicates based on theatre_name, date, and time, keeping the last occurrence
    df = df.drop_duplicates(subset=['Theatre Name', 'Date', 'Time'], keep='last')

    # Save the updated DataFrame back to the CSV file
    df.to_csv(file_path, index=False)
    print(f"Updated CSV file saved with {len(df)} records.")

with open('venky_vinayaka_29_Nov_6_30_PM.html', 'r', encoding='utf-8') as file:
    html_content = file.read()
  # Replace with your actual HTML

soup = BeautifulSoup(html_content, 'html.parser')


header_cont=soup.find("div",class_="header-container")
movie_name_element=header_cont.find("a",id="strEvtName")
theatre_name_element=header_cont.find("span",id="strVenName")
date_element=header_cont.find("span",id="strDate")
movie_name=movie_name_element.text.strip()
theatre_name=theatre_name_element.text.strip()
date_elements=date_element.text.strip().split(",")
date_text=date_elements[1].strip().replace(" ","_")
show_time=date_elements[-1].strip().replace(":","_").replace(" ","_")
print(movie_name_element.text)
print(theatre_name_element.text)
print(date_element.text)

file_name = f"{movie_name}/{movie_name.replace(' ', '_').replace(',', '_').replace('/', '-').replace(':', '-')}_{theatre_name.replace(' ', '_').replace(',', '_').replace('/', '-').replace(':', '-')}_{date_text}_{show_time}.csv"
metrics_file_name=f"{movie_name}/{movie_name.replace(' ', '_').replace(',', '_').replace('/', '-').replace(':', '-')}_{theatre_name.replace(' ', '_').replace(',', '_').replace('/', '-').replace(':', '-')}_{date_text}_{show_time}_metrics.csv"

m_name=movie_name.replace(' ', ' ').replace(',', ' ').replace('/', ' ').replace(':', ' ')
stats_file_name = f"{m_name}/{movie_name}.csv";
try:
    os.mkdir(m_name)
    print("Directory created successfully!")
except FileExistsError:
    print("Directory already exists.")
except OSError:
    print("Error creating directory. Please check permissions.")


# Find all the seat categories and their details
trows = soup.find_all('tr')
print(len(trows))
rows_data = []
Category_Price=dict()
Category_Count=dict()

current_category=None

for trow in trows:
    # Extracting the seat category
    #print(trow)
    tdata = trow.find('td',class_="PriceB1")
    if(tdata):
        div_text=tdata.find('div',class_="seatP").text.strip()
        div_text=div_text.replace("Rs. ","")
        cost_part, cat_part = div_text.split(' ', 1)
        try:
            Category_Price[cat_part]=float(cost_part)
        except:
            cat_part=div_text
            Category_Price[cat_part] = 100
        Category_Count[cat_part]={'available':0,'blocked':0}
        current_category=cat_part
        print(cost_part,cat_part)
    else:
        try:
            row_text=trow.find('div',"seatR Setrow1").text.strip();
            if(row_text==''):
                continue
        except :
            #print("Exception")
            continue
        #print(current_category,row_text,end=" ----- > ")

        blocked_as=trow.find_all('a',class_='_blocked')
        available_as=trow.find_all('a',class_="_available")

        blocked_as_count=0
        available_as_count=0

        if(blocked_as):blocked_as_count=len(blocked_as)
        if(available_as):available_as_count=len(available_as);
        Category_Count[current_category]['available']+=available_as_count
        Category_Count[current_category]['blocked'] += blocked_as_count

        #print("Available : ",available_as_count,"Blocked : ",blocked_as_count)
        #print("Cost Availble : ",Category_Price[current_category])

        row_price = Category_Price[current_category]
        available_cost = available_as_count * row_price
        unavailable_cost = blocked_as_count * row_price

        # Append row data to the list
        rows_data.append({
            'Class': current_category,
            'Row': row_text,
            'Price': row_price,
            'Available_count': available_as_count,
            'Booked_count': blocked_as_count,
            'Available_cost': available_cost,
            'Booked_cost': unavailable_cost
        })

print(Category_Count)
df = pd.DataFrame(rows_data)
df.to_csv(file_name, index=False)


# Initialize list to store the data for DataFrame
mets_data = []

# Process each seat class and calculate the values
for seat_class, seat_info in Category_Count.items():
    total_tickets = seat_info['available'] + seat_info['blocked']
    available_tickets = seat_info['available']
    unavailable_tickets = seat_info['blocked']

    # Calculate costs
    price_per_ticket = Category_Price.get(seat_class, 0)
    total_ticket_cost = total_tickets * price_per_ticket
    available_ticket_cost = available_tickets * price_per_ticket
    unavailable_ticket_cost = unavailable_tickets * price_per_ticket

    # Append data for this row
    mets_data.append({
        'Seat Class': f"{seat_class}_{price_per_ticket}",
        'Total Tickets': total_tickets,
        'Total Booked Tickets': unavailable_tickets,
        'Total Available Tickets': available_tickets,
        'Total Tickets Cost': total_ticket_cost,
        'Total Booked Tickets Cost': unavailable_ticket_cost,
        'Total Available Tickets Cost': available_ticket_cost

    })

# Convert list to DataFrame
mets_df = pd.DataFrame(mets_data)

# Calculate the total row
total_row = {
    'Seat Class': 'TOTAL',
    'Total Tickets': mets_df['Total Tickets'].sum(),
    'Total Booked Tickets': mets_df['Total Booked Tickets'].sum(),
    'Total Available Tickets': mets_df['Total Available Tickets'].sum(),
    'Total Tickets Cost': mets_df['Total Tickets Cost'].sum(),
    'Total Booked Tickets Cost': mets_df['Total Booked Tickets Cost'].sum(),
    'Total Available Tickets Cost': mets_df['Total Available Tickets Cost'].sum()

}
total_row_df = pd.DataFrame([total_row])

# Use pd.concat() to append the total row
mets_df = pd.concat([mets_df, total_row_df], ignore_index=True)

# Append the total row to the DataFrame
#mets_df = mets_df.append(total_row, ignore_index=True)


# Save DataFrame to CSV
mets_df.to_csv(metrics_file_name, index=False)
metrics = mets_df.iloc[-1]
current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
metrics_data = [{
        'Theatre Name': theatre_name,
        'Date': date_text,
        'Time': show_time,
        'Total Tickets': metrics['Total Tickets'],
        'Total Booked Tickets': metrics['Total Booked Tickets'],
        'Total Available Tickets': metrics['Total Available Tickets'],
        'Total Tickets Cost': metrics['Total Tickets Cost'],
        'Total Booked Tickets Cost': metrics['Total Booked Tickets Cost'],
        'Total Available Tickets Cost': metrics['Total Available Tickets Cost'],
        'Updated Time': current_time
    }]
update_movie_stats_csv(stats_file_name, metrics_data)


# Display the DataFrame
#print(df)



