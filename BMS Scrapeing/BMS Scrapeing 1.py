from selenium import webdriver
from selenium.webdriver.common.by import By
import  time
driver = webdriver.Chrome()

# Navigate to the target URL
url = 'https://in.bookmyshow.com/buytickets/the-greatest-of-all-time-bengaluru/movie-bang-ET00401439-MT/20240920#!seatlayout'
driver.get(url)

time.sleep(10)
# Wait for the page to load (can add waits here if needed)

# Extract the movie name
movie_name = driver.find_element(By.CSS_SELECTOR, '.cinema-name-wrapper a').text.strip()
print(movie_name)
# Extract theater details and show timings
theaters = driver.find_elements(By.CSS_SELECTOR, 'ul#venuelist li')
print(len(theaters))
# Create an empty list to store results
results = []

# Loop through each theater
for theater in theaters:
    theater_name = theater.get_attribute('data-name').strip()  # Extract the theater name
    print(theater_name,end="----")

    #if(theater_name=='Anjan Digital 4K A/C Cinema: Magadi Road'):
    #    print("Anjan Show is Available")
    #    break

    # Find all available showtimes for this theater
    showtimes = theater.find_elements(By.CSS_SELECTOR, '.showtime-pill-container a')

    # Iterate over each showtime-pill element
    for showtime in showtimes:

        # Find the child div with class 'sc-1isv5ko-2 eVvdFV' inside the showtime-pill element
        showtime_text = showtime.find_element(By.CSS_SELECTOR, 'div.__text').text.strip()

        # Extract the showtime text (e.g., '09:50 PM') from the div
        #time = time_element.text.strip()

        print(showtime_text,end=" , ")

        '''
        try:
            showtime.click()
            time.sleep(10)
        except:
            print("Click Failed")
        '''

    print()

# Close the browser
driver.quit()

# Print the extracted results
for detail in results:
    print(detail)
