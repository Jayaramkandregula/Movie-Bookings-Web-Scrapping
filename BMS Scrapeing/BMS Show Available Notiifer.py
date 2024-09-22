from selenium import webdriver
from selenium.webdriver.common.by import By
import pywhatkit as kit
import datetime
import time

from sympy.physics.units import seconds


def send_whatsapp_msg(msg):
    phone_numbers = ['+917675852443']  # Add more numbers as needed
    message = msg

    # Get current time and calculate the time to send the message (1 minute from now)
    now = datetime.datetime.now()
    hour = now.hour

    minute = now.minute + 1  # Send after one minute

    # Adjust for minute overflow
    if minute == 60:
        minute = 0
        hour += 1
    if hour == 24:
        hour = 0

    # Send messages to all phone numbers
    for number in phone_numbers:
        print(f"Sending message to {number}...")
        kit.sendwhatmsg(number, message, hour, minute)
        minute = minute + 2
        if minute == 60:
            minute = 0
            hour += 1
        if hour == 24:
            hour = 0

        time.sleep(1)  # Wait a few seconds before sending the next message

pref_theatres=['Anjan Digital 4K A/C Cinema: Magadi Road','Sri Vinayaka Marathahalli 4k A/C Dolby Atmos']
#pref_theatres=['Vaibhav Cinemas A/C 4K 7.1 Dolby: Doddaballapura','Sri Vinayaka Marathahalli 4k A/C Dolby Atmos']
pref_theat_found= {pref_theatres[0]:0,pref_theatres[1]:0}
pref_theat_pref_show_found={pref_theatres[0]:0,pref_theatres[1]:0}
count=0

found_count=0
while (True):
    driver = webdriver.Chrome()
    movie_name=""
    # Navigate to the target URL
    url = 'https://in.bookmyshow.com/buytickets/devara-part-1-bengaluru/movie-bang-ET00310216-MT/20240927'
    driver.get(url)
    movie_name = driver.find_element(By.CSS_SELECTOR, '.cinema-name-wrapper a').text.strip()

    print(movie_name)

    theaters = driver.find_elements(By.CSS_SELECTOR, 'ul#venuelist li')
    print(len(theaters))
    # Create an empty list to store results
    found=0
    # Loop through each theater
    pref_dict=dict()

    msg=""
    for theater in theaters:
        theater_name = theater.get_attribute('data-name').strip()  # Extract the theater name
        print(theater_name)

        if (theater_name in pref_theatres):
            print(theater_name,"Show is Available")
            # Find all available showtimes for this theater
            showtimes = theater.find_elements(By.CSS_SELECTOR, '.showtime-pill-container a')
            showtimesList=[]
            # Iterate over each showtime-pill element
            pref_show_time=""
            for showtime in showtimes:
                # Find the child div with class 'sc-1isv5ko-2 eVvdFV' inside the showtime-pill element
                showtime_text = showtime.find_element(By.CSS_SELECTOR, 'div.__text').text.strip()
                st=showtime_text.replace(":"," ").split(" ")
                if((st[0]=='01' or st[0]=='12' or st[0]=='00') and st[2]=='AM'):
                    pref_show_time=showtime_text
                #print(showtime_text, end=" , ")
                showtimesList.append(showtime_text)

            pref_dict[theater_name]=showtimesList
            if(pref_show_time!=""):
                if(pref_theat_pref_show_found[theater_name]<=2):
                    found=1
                    msg+=f"{pref_show_time} Show is Available\n{theater_name}\n{movie_name}\nBookings Available\n\n"
                pref_theat_pref_show_found[theater_name]=pref_theat_pref_show_found[theater_name]+1

            else:
                if (pref_theat_found[theater_name] < 2):
                    msg += f"{theater_name}\n{','.join(showtimesList)}\n{movie_name}\nBookings Available\n\n"
                    found = 1
            pref_theat_found[theater_name] += 1
    if (found == 1):
        print(msg)
        print(pref_theat_found, pref_theat_pref_show_found)
        try:
            send_whatsapp_msg(msg + "URL : " + url)
        except:
            print("Whatsapp message Exception")
    else:
        less=0
        for k in list(pref_theat_found.values()):
            if(k<2):
                less+=1
                break
        for k in list(pref_theat_pref_show_found.values()):
            if(k<2):
                less+=1
                break
        if(less==0):
            break

    count+=1
    print("Successfully Executed  : ",count,"Times\n\n")


    time.sleep(50)


"""


print("All messages sent!")
"""

"""
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

    if(theater_name=='Anjan Digital 4K A/C Cinema: Magadi Road'):
        print("Anjan Show is Available")
        break

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
"""




# Email configuration


# Create the email



# List of phone numbers (in international format)