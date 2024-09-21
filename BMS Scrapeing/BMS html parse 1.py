from bs4 import BeautifulSoup
from shapely.speedups import available

with open('demo.html', 'r', encoding='utf-8') as file:
    html_content = file.read()
  # Replace with your actual HTML

soup = BeautifulSoup(html_content, 'html.parser')


header_cont=soup.find("div",class_="header-container")
movie_name_element=header_cont.find("a",id="strEvtName")
theatre_name_element=header_cont.find("span",id="strVenName")
date_element=header_cont.find("span",id="strDate")
print(movie_name_element.text)
print(theatre_name_element.text)
print(date_element.text)


# Find all the seat categories and their details
trows = soup.find_all('tr')
print(len(trows))

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
        Category_Price[cat_part]=cost_part
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
        print(current_category,row_text,end=" ----- > ")

        blocked_as=trow.find_all('a',class_='_blocked')
        available_as=trow.find_all('a',class_="_available")

        blocked_as_count=0
        available_as_count=0

        if(blocked_as):blocked_as_count=len(blocked_as)
        if(available_as):available_as_count=len(available_as);
        

        print("Available : ",available_as_count,"Blocked : ",blocked_as_count)




        #print(tdata)
    #print(len(tdata))
    # Find all rows for this category
    #seats_rows = category.find_next_siblings('tr')

    #print(f"Category: {category_text}")

    """
    for row in seats_rows:
        # Skip empty rows
        if row.find('td', class_='SRow1'):
            seat_cells = row.find_all('div', class_='seatI')
            for cell in seat_cells:
                if cell.a:  # If the cell has a link (meaning it is a seat)
                    seat_number = cell.a.text.strip()
                    seat_status = 'Available' if '_available' in cell.a['class'] else 'Blocked'
                    print(f"  Seat {seat_number}: {seat_status}")

    print()  # Newline for better readability """
