from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import csv
import re

# Setup Chrome WebDriver (Download the appropriate driver from https://chromedriver.chromium.org/)
driver = webdriver.Chrome()

# Open the Paytm movie booking page
driver.get("https://paytm.com/movies/seat-layout/bengaluru/b_odqglzc?encsessionid=1020740-8990-ob0dbh-1020740&freeseating=false&fromsessions=true")

# Allow time for the page to fully load
time.sleep(20)  # Adjust sleep time based on page load speed

# Extract Movie Name
movie_name = driver.find_element(By.CLASS_NAME, "textClamp").text

# Extract Theater Name
theater_name = driver.find_element(By.XPATH, '//h3').text
print(movie_name,theater_name);

# Find all showtimes
showtimes = driver.find_elements(By.CLASS_NAME, "SeatLayoutHeader_time__AFJX0")
print(len(showtimes))

for showtime_element in showtimes:
    # Extract showtime text
    show_time = showtime_element.text


    # Create a valid CSV filename for each showtime
    safe_show_time = re.sub(r'[\/:*?"<>|\n]', '-', show_time)  # Replace invalid characters
    file_name = f"{movie_name.replace(' ', '_').replace(',', '_').replace(' ', '_').replace('/', '-').replace(':', '-')}_{theater_name.replace(' ', '_').replace(',', '_').replace('/', '-').replace(':', '-')}_{safe_show_time}_extracted_time_{time.ge}_.csv"
    print(file_name)
    # Click on the showtime to load the seat map
    showtime_element.click()

    # Allow time for the seat map to load
    time.sleep(20)  # Adjust sleep time based on page load speed

    # Open a CSV file to write data for the current showtime
    with open(file_name, mode='w', newline='') as file:
        writer = csv.writer(file)
        # Write header row
        writer.writerow(['Seat Class', 'Row', 'Column', 'Seat Number', 'Availability Status'])

        # Find all available and unavailable seats
        all_seats = driver.find_elements(By.XPATH, '//span[contains(@aria-label, "seat")]')

        # Process each seat and extract details
        for seat in all_seats:
            aria_label = seat.get_attribute("aria-label")  # Extract the aria-label attribute
            # Split the aria-label into components
            components = aria_label.split(',')

            # Extract the seat class, row, column, and price if available
            seat_class = components[1].split()[-1]  # Extract seat class (e.g., GOLD)
            row = components[2].split()[-1]  # Extract row information (e.g., A)
            column = components[3].split()[-1]  # Extract column number (e.g., 13)

            # Extract seat number from the label tag, if present
            try:
                seat_number = seat.find_element(By.TAG_NAME, 'label').text.strip()  # Extract seat number
            except:
                seat_number = ""  # If no seat number is found, leave it empty

            # Determine availability based on class name
            if "available" in seat.get_attribute("class"):
                availability_status = "Available"
            else:
                availability_status = "Unavailable"

            # Write the extracted seat details to the CSV file
            writer.writerow([seat_class, row, column, seat_number, availability_status])

# Close the browser after completion
driver.quit()
'''
# Extract Show Time
show_time = driver.find_element(By.CLASS_NAME, "SeatLayoutHeader_time__AFJX0").text

# Print the extracted movie details
print(f"Movie Name: {movie_name}")
print(f"Theater Name: {theater_name}")
print(f"Show Time: {show_time}")

# Find all available and unavailable seats (using span with "aria-label" for seats)
all_seats = driver.find_elements(By.XPATH, '//span[contains(@aria-label, "seat")]')

# Process each seat and extract details
for seat in all_seats:
    aria_label = seat.get_attribute("aria-label")  # Extract the aria-label attribute
    # Split the aria-label into components
    components = aria_label.split(',')

    # Extract the seat class, row, column, and price if available
    seat_class = components[1].split()[-1]  # Extract seat class (e.g., GOLD)
    row = components[2].split()[-1]  # Extract row information (e.g., A)
    column = components[3].split()[-1]  # Extract column number (e.g., 13)

    # Extract seat number from the label tag, if present
    try:
        seat_number = seat.find_element(By.TAG_NAME, 'label').text.strip()  # Extract seat number
    except:
        seat_number = ""  # If no seat number is found, leave it empty

    # Determine availability based on class name
    if "available" in seat.get_attribute("class"):
        availability_status = "Available"
    else:
        availability_status = "Unavailable"

    # Print the extracted seat details in the required format
    print(
        f"Seat Class: {seat_class}, Row: {row}, Column: {column}, Seat Number: {seat_number}, Availability: {availability_status}")

# Close the browser after completion
driver.quit()'''
# Example: Extract seat layout details - check if seats are marked as booked
'''total_seats = driver.find_elements(By.CLASS_NAME, 'FixedSeating_tooltipWrap__PtsaD')  # Change the class name based on the actual class used for seats

booked_count = 0

for seat in total_seats:
    if 'FixedSeating_disable__UH76Z' in seat.get_attribute('class'):  # Check if the seat has the 'booked' class
        booked_count += 1

print(f"Total booked seats: {booked_count}")
print(len(total_seats))
# Close the driver after extraction
driver.quit()'''
