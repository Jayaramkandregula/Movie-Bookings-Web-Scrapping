from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import csv
import re
import pandas as pd
from datetime import datetime
import os


def process_prices(df):
    # Ensure the 'Price' column is numeric and replace invalid entries with -1
    df['Price'] = pd.to_numeric(df['Price'], errors='coerce').fillna(-1).astype(int)

    # Extract unique seat classes
    seat_classes = df['Seat Class'].unique()

    # Initialize the price mapping dictionary
    price_mapping = {}

    # Extract price mapping from DataFrame
    for seat_class in seat_classes:
        # Get the non-"NA" prices for the current seat class
        class_prices = df[(df['Seat Class'] == seat_class) & (df['Price'] != -1)]['Price'].dropna().unique()

        # If there are any non-"NA" prices, take the first one as the default price
        if len(class_prices) > 0:
            price_mapping[seat_class] = class_prices[0]
        else:
            # If all prices are "NA", ask the user for the price for this seat class
            while True:
                try:
                    user_input = float(input(f"Please enter the price for seat class '{seat_class}': "))
                    price_mapping[seat_class] = user_input
                    break
                except ValueError:
                    print("Invalid input. Please enter a numeric value.")

    # Replace -1 in the Price column with the seat class price from the price_mapping dictionary
    df['Price'] = df.apply(
        lambda row: price_mapping.get(row['Seat Class'], -1) if row['Price'] == -1 else row['Price'],
        axis=1
    )

    return df

import pandas as pd

def calculate_metrics(df):
    # Group by 'Seat Class' and calculate statistics
    grouped_df = df.groupby('Seat Class').agg(
        total_tickets=('Seat Class', 'size'),
        available_tickets=('Availability Status', lambda x: (x == 'Available').sum()),
        unavailable_tickets=('Availability Status', lambda x: (x == 'Unavailable').sum()),
        total_ticket_cost=('Price', 'sum'),
        available_ticket_cost=('Price', lambda x: x[df['Availability Status'] == 'Available'].sum()),
        unavailable_ticket_cost=('Price', lambda x: x[df['Availability Status'] == 'Unavailable'].sum())
    ).reset_index()

    # Calculate the total sum of all tickets' costs and counts
    total_tickets = grouped_df['total_tickets'].sum()
    available_tickets = grouped_df['available_tickets'].sum()
    unavailable_tickets = grouped_df['unavailable_tickets'].sum()
    total_costs = grouped_df['total_ticket_cost'].sum()
    available_costs = grouped_df['available_ticket_cost'].sum()
    unavailable_costs = grouped_df['unavailable_ticket_cost'].sum()

    # Create the total row
    total_row = pd.DataFrame({
        'Seat Class': ['TOTAL'],
        'total_tickets': [total_tickets],
        'available_tickets': [available_tickets],
        'unavailable_tickets': [unavailable_tickets],
        'total_ticket_cost': [total_costs],
        'available_ticket_cost': [available_costs],
        'unavailable_ticket_cost': [unavailable_costs]
    })

    # Drop columns with NaN values in total_row
    total_row = total_row.fillna(0)

    # Append the total row to the grouped DataFrame
    final_df = pd.concat([grouped_df, total_row], ignore_index=True)

    return final_df


# Define the columns for the CSV file
columns = [
    'Theatre Name',
    'Date',
    'Time',
    'Total Tickets',
    'Unavailable Tickets',
    'Available Tickets',
    'Total Tickets Cost',
    'Total Unavailable Tickets Cost',
    'Total Available Tickets Cost',
    'Updated Time'
]


# Function to check if the file exists and create it if necessary
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


driver = webdriver.Edge()
url = "https://paytm.com/movies/seat-layout/bengaluru/tqh6qs8nl?encsessionid=43628-30693__1726880400__50__16698-ob17yh-43628&freeseating=false&fromsessions=true"
# Open the Paytm movie booking page
driver.get(url)

# Allow time for the page to fully load
time.sleep(10)  # Adjust sleep time based on page load speed

# Extract Movie Name
movie_name = driver.find_element(By.CLASS_NAME, "textClamp").text

m_name=movie_name.replace(' ', ' ').replace(',', ' ').replace('/', ' ').replace(':', ' ')

try:
    os.mkdir(m_name)
    print("Directory created successfully!")
except FileExistsError:
    print("Directory already exists.")
except OSError:
    print("Error creating directory. Please check permissions.")

# Extract Theater Name
theater_name = driver.find_element(By.XPATH, '//h3').text
print(movie_name, theater_name)

bookings_date = driver.find_element(By.CLASS_NAME, "SeatLayoutHeader_sessionDate__D84BZ").text
bookings_date = re.sub(r'[\/:*?"<>|\n]', '-', bookings_date)

print(bookings_date)

stats_file_name = f"{m_name}/{movie_name}.csv";

# Find all showtimes
showtimes = driver.find_elements(By.CLASS_NAME, "SeatLayoutHeader_time__AFJX0")
print(len(showtimes))

# Initialize a list to hold data for the DataFrame


for showtime_element in showtimes:
    # Extract showtime text
    show_time = showtime_element.text

    # Sanitize showtime for filename
    safe_show_time = re.sub(r'[\/:*?"<>|\n]', '-', show_time)  # Replace invalid characters
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_name = f"{m_name}/{movie_name.replace(' ', '_').replace(',', '_').replace('/', '-').replace(':', '-')}_{theater_name.replace(' ', '_').replace(',', '_').replace('/', '-').replace(':', '-')}_{bookings_date}_{safe_show_time}.csv"
    metrics_file_name = f"{m_name}/{movie_name.replace(' ', '_').replace(',', '_').replace('/', '-').replace(':', '-')}_{theater_name.replace(' ', '_').replace(',', '_').replace('/', '-').replace(':', '-')}_{bookings_date}_{safe_show_time}_metrics.csv"
    print(file_name)

    # Click on the showtime to load the seat map
    showtime_element.click()

    # Allow time for the seat map to load
    time.sleep(10)  # Adjust sleep time based on page load speed

    # Find all available and unavailable seats
    all_seats = driver.find_elements(By.XPATH, '//span[contains(@aria-label, "seat")]')
    seat_data = []
    # Process each seat and extract details
    for seat in all_seats:
        aria_label = seat.get_attribute("aria-label")  # Extract the aria-label attribute
        # Split the aria-label into components
        components = aria_label.split(',')

        # Extract the seat class, row, column, and price if available
        seat_class = components[1].replace('class','').strip()  # Extract seat class (e.g., GOLD)
        row = components[2].split()[-1]  # Extract row information (e.g., A)
        column = components[3].split()[-1]  # Extract column number (e.g., 13)

        try:
            # Extract the price and remove non-numeric characters using regex
            price = re.sub(r'\D', '', components[4].strip())

            # Convert price to an integer, or set it to -1 if it's empty
            price = int(price) if price else -1
        except IndexError:
            price = -1  # If no price is found, assign -1

        # Extract price if available

        # Extract seat number from the label tag, if present
        try:
            seat_number = seat.find_element(By.TAG_NAME, 'label').text.strip()  # Extract seat number
        except:
            seat_number = "NA"  # If no seat number is found, leave it empty

        # Determine availability based on class name
        if "available" in seat.get_attribute("class"):
            availability_status = "Available"
        else:
            availability_status = "Unavailable"

        # Append seat details to the list
        seat_data.append([seat_class, row, column, seat_number, availability_status, price])

    # Convert the list to a DataFrame
    df = pd.DataFrame(seat_data, columns=['Seat Class', 'Row', 'Column', 'Seat Number', 'Availability Status', 'Price'])

    df = process_prices(df)

    # Save the DataFrame to a CSV file
    df.to_csv(file_name, index=False)

    mets_df = calculate_metrics(df)

    mets_df.to_csv(metrics_file_name, index=False)
    metrics = mets_df.iloc[-1]
    metrics_data = [{
        'Theatre Name': theater_name,
        'Date': bookings_date,
        'Time': show_time,
        'Total Tickets': metrics['total_tickets'],
        'Unavailable Tickets': metrics['unavailable_tickets'],
        'Available Tickets': metrics['available_tickets'],
        'Total Tickets Cost': metrics['total_ticket_cost'],
        'Total Unavailable Tickets Cost': metrics['unavailable_ticket_cost'],
        'Total Available Tickets Cost': metrics['available_ticket_cost'],
        'Updated Time': current_time
    }]

    update_movie_stats_csv(stats_file_name, metrics_data)
    # metrics_df = pd.DataFrame([metrics_data])

# Close the browser after completion
driver.quit()

