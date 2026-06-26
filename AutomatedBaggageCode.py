import turtle
import math

# Function 1 - Passenger Data
def passenger_data():
    """This function reads passenger information from 'passenger_data.txt' and converts it into a 2D list. 
    Each inner list represents a passenger's details, including name, first letter of last name, 
    gate, seating class, destination, arrival status, baggage weight, and layover status. 
    It returns a 2D list where each sublist contains the details of one passenger."""
    
    passenger_list=[] #empty list to store passenger info
    file_obj=open('passenger_data_v1 (1).txt', 'r') #open file
    
    for line in file_obj:
        separated_line=line.strip() #separate lines

        if len(separated_line)>0: #if line is not empty
            info=separated_line.split(',') #split info by commas
            
            #all of the passenger's info is in the following order:
            #name, last name, gate, seating class, destination, arrival status, baggage weight, layover status
                
            name=info[0]  #name of passenger
            last_initial=info[1][0]  #first character of passenger's last name (first entry in inner list, second entry in outer list)
            gate=info[2]
            seating_class=info[3]  
            destination=info[4]
            arrival_status=info[5]
            baggage_weight=float(info[6]) # originally a string
            layover_status=info[7] 
            
            passenger_list.append([name, last_initial, gate, seating_class, destination, arrival_status, baggage_weight, layover_status]) 
            #append data of each passenger as a list inside main list
            
    file_obj.close()

    if len(passenger_list)==0: #check if passenger_list is empty
        print("Error. No data available in Passenger Data file.")
        return None
    else:
       print(passenger_list)
       return passenger_list #return passenger data list
   
    
# Function 2 - Fleet Data
def fleet_data():
    """This function reads information from 'fleet_data.txt' and converts it into a 2D list. 
    Each inner list represents details for an individual plane, including model, 
    number of business and economy seats, total seats, gate, destination, 
    arrival status, and maximum baggage weight allowed per passenger. 
    It returns a 2D list where each sublist contains the details of one plane. """ 
   
    file_obj= open('fleet_data.txt')
    fleet_list=[] #define list that will be returned
   
    for line in file_obj:  #goes through every line in the file
        placeholder=line.strip() # removes whitespace from the line
        temp_list=placeholder.split(',') # splits the line by commas- creates list of elements
        
        # converts following info to integers:
        temp_list[1] = int(temp_list[1]) # business seats
        temp_list[2] = int(temp_list[2]) # economy seats
        temp_list[3] = int(temp_list[3]) # total number seats
        temp_list[7] = int(temp_list[7]) # max baggage weight
        
        fleet_list.append(temp_list)
    
    file_obj.close()
    
    return fleet_list
    
# Function 3 - Daily Data

def daily_data(passenger_list):
    """ This function counts the number of business and economy seats sold for 
    each gate based on passenger data. This function processes a 2D list of passenger 
    info, counting seat counts by gate and seating class. It returns a 2D list 
    with each entry showing the gate, the number of business passengers, and 
    the number of economy passengers."""

    daily_data_result=[] #empty list to store count of business and economy seats per gate
    
    for passenger in passenger_list: #for all entries in passenger data
        gate=passenger[2] # gate is third piece of info listed
        seat_type=passenger[3] #seat is 4th

        #check whether this gate is already in results list or not
        for i in daily_data_result:
            if i[0]==gate: #if it is already there - add to count of the corresponding seat type
                if seat_type=="B":
                    i[1]+= 1
                elif seat_type=="E":
                    i[2]+= 1 
                break
        
        else: #if the gate is not already in daily_data_result, add new entry
        
        #if above block is true it will go through break statement and skip the 'else' block
        #if above block is false, break statement is not executed, and 'else' block is read

            if seat_type=="B": #add to business seat count
                daily_data_result.append([gate,1,0]) #1 business; 0 economy
            elif seat_type=="E":
                daily_data_result.append([gate,0,1]) #0 business;1 economy

    print(daily_data_result)
    return daily_data_result

# Function 4 - Oversold

def oversold(passenger_data_result, fleet_data_result, daily_data_result):
    """This function creates two 2D lists indicating oversold seats for each flight.
    The first list includes each plane's model and the number of oversold business seats.
    The second list includes each plane's model and the number of oversold economy seats.
    It takes output from passenger_data(), fleet_data(), and daily_data() as input."""
    
    
    business_class_oversold=[]
    economy_class_oversold=[]
    

    for plane in fleet_data_result:
        for gate in daily_data_result:
            if gate[0] == plane[4]: #checks if the gate numbers match 
                temp_list_economy = [plane[0], a] #automatically defines the first term in the list to be the plane's model
                temp_list_business = [plane[0], a]
                oversold_business = 0
                oversold_economy = 0
                if plane[1] < gate[1]: #if there's less seats on the plane than tickets sold
                    oversold_business = gate[1] - plane[1]  #this code won't execute unless there's more booked seats than available
                temp_list_business[1] = oversold_business #edits the 2nd term of the list
                
                if plane[2] < gate[2]:
                    oversold_economy = gate[2] - plane[2]
                temp_list_economy[1] = oversold_economy
                
                business_class_oversold.append(temp_list_business)
                economy_class_oversold.append(temp_list_economy)
    return business_class_oversold , economy_class_oversold
    #returns both lists

# Function 5 - Overweight

def overweight(passenger_list,fleet_list):
    """ This function creates two 2D lists indicating passengers with overweight baggage for each flight.
    The first list includes each plane's model and the count of passengers exceeding the allowed baggage weight.
    The second list includes details of each overweight passenger, including first name, first letter of last name,
    gate, and the excess baggage weight to one decimal place. It takes output from passenger_data() and fleet_data() as input."""
                
    flight_weight_stats=[] #list to store the number of overweight passengers for each flight
    overweight_passengers=[] #list to store details of passengers with overweight baggage.

    for i in range(len(fleet_list)): #for each plane in fleet data
        number_of_overweight_passengers=0 #counts number of overweight passengers on current flight

        for z in range(len(passenger_list)):  # Check each passenger
            if fleet_list[i][4]==passenger_list[z][2]:  # make sure gate number of the plane matches the passenger's gate number
                max_weight=int(fleet_list[i][7])  # max baggage weight allowed for the plane
                passenger_weight=passenger_list[z][6]  # baggage weight of the current passenger 

                if passenger_weight>max_weight:  # if passenger's baggage weighs more than max
                    number_of_overweight_passengers+=1 

                    passenger_name=passenger_list[z][0]
                    first_letter_last_name=passenger_list[z][1][0]  #first letter of last name
                    gate_number=passenger_list[z][2]
                    weight_overweight = round(passenger_weight - max_weight, 1)

                    overweight_passengers.append([
                        passenger_name, 
                        first_letter_last_name, 
                        gate_number, 
                        weight_overweight
                    ])

        plane_model = fleet_list[i][0]
        flight_weight_stats.append([plane_model, number_of_overweight_passengers])

    return flight_weight_stats, overweight_passengers


# Function 6 - Layover Function  
       
def layover(passenger_list, fleet_list):
    """This function calculates the number of passengers with a layover for each plane in the fleet.
    It takes lists of passenger and fleet details, matches each passenger to their plane's gate, 
    and counts those with a layover. It returns a 2D list with each plane model and its layover passenger count
    as well as a 2D list with individual passenger layover details."""
    
    layover_passenger_list = []  # empty list to store layover info
    layover_passenger_details = []  # empty list to store individual layover passenger details

    # go through each plane:
    for plane in fleet_list:
        model = plane[0]  # model of plane is first entry in fleet_list
        layover_count = 0  # reset layover count for each plane
        
        for passenger in passenger_list:  # go through each passenger in each plane
            if passenger[2] == plane[4] and passenger[7] == "Layover":  # match gate and layover status 
                layover_count += 1  # if passenger has layover
                
                # get details of each passenger with a layover
                passenger_name = passenger[0]
                last_initial = passenger[1] #letter of passenger's last name
                gate = passenger[2] #their gate
                layover_passenger_details.append([passenger_name, last_initial, gate])
        
        # append the model and count of amount of layover passengers to the layover list, with sublists
        layover_passenger_list.append([model, layover_count])
    
    return layover_passenger_list, layover_passenger_details  # output layover list and passenger details

# Function 7 - Time Delay

def time_delay(fleet_list, passenger_list):
    """ This function calculates the number of passengers on each flight who are 
    both late and have a layover. This function processes fleet and passenger 
    data to produce a 2D list containing each plane's model and the count of 
    passengers with a "Late" arrival status and "Layover" status."""

    time_delay_data=[]

    for plane in fleet_list: # for each plane in fleet data
        plane_model=plane[0]  #plane model is first part of the list
        flight_number=plane[4]  #flight number is fifth part of list
        flight_count=0  #counts passengers
        
        for passenger in passenger_list: #for each passenger
            p_flight_number=passenger[2]  #passenger's flight number is third
            passenger_status=passenger[5]  #late is sixth
            layover_status=passenger[7]  #layover is eigth
            
            #check both late and layover:
            if p_flight_number==flight_number:
                if passenger_status=="Late" and layover_status=="Layover":
                    flight_count+=1
        
        #add results to time_delay_data list
        time_delay_data.append([plane_model, flight_count])

    return time_delay_data

# Function 8 - Graphical Team ID

# screen set up
SCREEN_WIDTH = 2200
SCREEN_HEIGHT = 800
WINDOW_TITLE = "International Airport"
BACKGROUND_COLOR = "lightblue"

screen = turtle.Screen()
screen.title(WINDOW_TITLE)
screen.bgcolor(BACKGROUND_COLOR)
screen.setup(SCREEN_WIDTH, SCREEN_HEIGHT)

def graphical_teamID(
    fleet_list, passenger_list, daily_data_result, time_delay_data,
    layover_passenger_list, layover_passenger_details, flight_weight_stats, overweight_passengers,
    oversold_business_class, oversold_economy):    
    """ This function generates a graphical summary of key information for airport operations.
    It helps visualize the number of oversold seats, passengers with overweight baggage, 
    passengers with layovers, and those arriving late with layovers for each plane. 
    It takes input from other functions such as, oversold(), overweight(), layover(), 
    and time_delay(). The information displayed as well as screen customizations are done 
    inside the function. Our team's extra graphical components were done outside of the function
    using helper code"""
    
    # turtle for text
    text_turtle = turtle.Turtle()
    text_turtle.speed(0)
    text_turtle.hideturtle()

    # box around title
    text_turtle.penup()
    text_turtle.goto(-80, 250)
    text_turtle.pensize(1)
    text_turtle.pencolor("grey")
    text_turtle.pendown()
    text_turtle.begin_fill()
    text_turtle.fillcolor("grey")
    text_turtle.right(180)
    text_turtle.forward(180)
    text_turtle.right(90)
    text_turtle.forward(70)
    text_turtle.right(90)
    text_turtle.forward(480)
    text_turtle.right(90)
    text_turtle.forward(70)
    text_turtle.right(90)
    text_turtle.forward(440)
    text_turtle.end_fill()

    # writing the title
    text_turtle.penup()
    text_turtle.pencolor("black")
    text_turtle.pensize(10)
    text_turtle.goto(-20, 270)
    text_turtle.pendown()
    text_turtle.write("Flight Passenger Summary", align="center", font=("Times New Roman", 14, "bold"))

    # coordinates to write info
    x_coords_list = []
    y_coords_list = []

    x_coord = -700
    y_coord = 100
    

    # all data into a list organized format
    planes_data = [
        [
            f"{fleet_list[0][0]}",
            f"Business Seats: {fleet_list[0][1]}",
            f"Economy Seats: {fleet_list[0][2]}",
            f"Total Seats: {fleet_list[0][3]}",
            f"Gate: {fleet_list[0][4]}",
            f"Destination: {fleet_list[0][5]}",
            f"Arrival Status: {fleet_list[0][6]}",
            f"Max Baggage Weight: {fleet_list[0][7]}",
            f"Oversold Business: {oversold_business_class[0][1]}",
            f"Oversold Economy: {oversold_economy[0][1]}",
            f"Overweight Passengers: {flight_weight_stats[0][1]}",
            f"Layover Passengers: {layover_passenger_list[0][1]}"
        ],
        [
            f"{fleet_list[1][0]}",
            f"Business Seats: {fleet_list[1][1]}",
            f"Economy Seats: {fleet_list[1][2]}",
            f"Total Seats: {fleet_list[1][3]}",
            f"Gate: {fleet_list[1][4]}",
            f"Destination: {fleet_list[1][5]}",
            f"Arrival Status: {fleet_list[1][6]}",
            f"Max Baggage Weight: {fleet_list[1][7]}",
            f"Oversold Business: {oversold_business_class[1][1]}",
            f"Oversold Economy: {oversold_economy[1][1]}",
            f"Overweight Passengers: {flight_weight_stats[1][1]}",
            f"Layover Passengers: {layover_passenger_list[1][1]}"
        ],
        [
            f"{fleet_list[2][0]}",
            f"Business Seats: {fleet_list[2][1]}",
            f"Economy Seats: {fleet_list[2][2]}",
            f"Total Seats: {fleet_list[2][3]}",
            f"Gate: {fleet_list[2][4]}",
            f"Destination: {fleet_list[2][5]}",
            f"Arrival Status: {fleet_list[2][6]}",
            f"Max Baggage Weight: {fleet_list[2][7]}",
            f"Oversold Business: {oversold_business_class[2][1]}",
            f"Oversold Economy: {oversold_economy[2][1]}",
            f"Overweight Passengers: {flight_weight_stats[2][1]}",
            f"Layover Passengers: {layover_passenger_list[2][1]}"
        ],
        [
            f"{fleet_list[3][0]}",
            f"Business Seats: {fleet_list[3][1]}",
            f"Economy Seats: {fleet_list[3][2]}",
            f"Total Seats: {fleet_list[3][3]}",
            f"Gate: {fleet_list[3][4]}",
            f"Destination: {fleet_list[3][5]}",
            f"Arrival Status: {fleet_list[3][6]}",
            f"Max Baggage Weight: {fleet_list[3][7]}",
            f"Oversold Business: {oversold_business_class[3][1]}",
            f"Oversold Economy: {oversold_economy[3][1]}",
            f"Overweight Passengers: {flight_weight_stats[3][1]}",
            f"Layover Passengers: {layover_passenger_list[3][1]}"
        ],
         [
            f"{fleet_list[4][0]}",
            f"Business Seats: {fleet_list[4][1]}",
            f"Economy Seats: {fleet_list[4][2]}",
            f"Total Seats: {fleet_list[4][3]}",
            f"Gate: {fleet_list[4][4]}",
            f"Destination: {fleet_list[4][5]}",
            f"Arrival Status: {fleet_list[4][6]}",
            f"Max Baggage Weight: {fleet_list[4][7]}",
            f"Oversold Business: {oversold_business_class[4][1]}",
            f"Oversold Economy: {oversold_economy[4][1]}",
            f"Overweight Passengers: {flight_weight_stats[4][1]}",
            f"Layover Passengers: {layover_passenger_list[4][1]}"
        ],
         [
            f"{fleet_list[5][0]}",
            f"Business Seats: {fleet_list[5][1]}",
            f"Economy Seats: {fleet_list[5][2]}",
            f"Total Seats: {fleet_list[5][3]}",
            f"Gate: {fleet_list[5][4]}",
            f"Destination: {fleet_list[5][5]}",
            f"Arrival Status: {fleet_list[5][6]}",
            f"Max Baggage Weight: {fleet_list[5][7]}",
            f"Oversold Business: {oversold_business_class[5][1]}",
            f"Oversold Economy: {oversold_economy[5][1]}",
            f"Overweight Passengers: {flight_weight_stats[5][1]}",
            f"Layover Passengers: {layover_passenger_list[5][1]}"
        ],
         [
            f"{fleet_list[6][0]}",
            f"Business Seats: {fleet_list[6][1]}",
            f"Economy Seats: {fleet_list[6][2]}",
            f"Total Seats: {fleet_list[6][3]}",
            f"Gate: {fleet_list[6][4]}",
            f"Destination: {fleet_list[6][5]}",
            f"Arrival Status: {fleet_list[6][6]}",
            f"Max Baggage Weight: {fleet_list[6][7]}",
            f"Oversold Business: {oversold_business_class[6][1]}",
            f"Oversold Economy: {oversold_economy[6][1]}",
            f"Overweight Passengers: {flight_weight_stats[6][1]}",
           f"Layover Passengers: {layover_passenger_list[6][1]}"
        ]]
    
    for plane in planes_data:
        text_turtle.pencolor("black")
        text_turtle.penup()
        ax=x_coord-90
        bx=y_coord
        text_turtle.goto(ax, bx)
        text_turtle.write(plane[0], align="center", font=("Times New Roman", 12, "bold"))

        # details of each plane under plane name  
        y_coord2 = bx - 40
        x_coord2 = ax - 12
        for info in plane[1:]:
            text_turtle.goto(x_coord2, y_coord2)
            text_turtle.write(info, align="center", font=("Times New Roman", 12, "normal"))
            y_coord2 -= 25

        # store airplane coordinates (100 units below each block of info)
        x_coords_list.append(x_coord)
        y_coords_list.append(y_coord2 - 50)

        # next column for next plane
        x_coord += 265
        

    return x_coords_list, y_coords_list

#call function to get the coordinates
a = fleet_data()  # fleet list from fleet_data function
b = passenger_data()  # passenger list from passenger_data function
c = daily_data(b)  # daily data using passenger list
d = time_delay(a, b)  # time delay data
e,f = layover(b, a)  # layover passenger list and details
g, h = overweight(b, a)  # overweight flight stats and passengers
i, j=oversold(b,a,c) #oversold 


x_coords_list, y_coords_list = graphical_teamID(a,b,c,d,e,f,g,h,i,j)

# draw airplanes below info
for z in range(len(x_coords_list)):
    # turtle to draw airplane
    oval_turtle = turtle.Turtle()
    oval_turtle.color("blue")
    oval_turtle.speed(0)
    screen.tracer(0)

    horizontal_radius_main = 20# horizontal radius for width
    vertical_radius_main = 100#vertical radius for height

    # draw oval body
    oval_turtle.penup() # get turtle at the starting point so airplane is drawn centered at x_coord point
    oval_turtle.goto(x_coords_list[z] + horizontal_radius_main, y_coords_list[z]-50)
    oval_turtle.pendown()
    oval_turtle.begin_fill()
    for angle in range(361): # to make smooth curve go through all 360 degrees
    #x and y coordinates for each angle calculated using parametric equations of an ellipse
        x = x_coords_list[z] + horizontal_radius_main * math.cos(math.radians(angle))
        # x=x_center+ horizontal_radius(cos(theta))
        y = y_coords_list[z]-50 + vertical_radius_main * math.sin(math.radians(angle))
        # y=y_center+ vertical_radius(sin(theta))
        oval_turtle.goto(x, y) #move turtle to calculated coordinates
    oval_turtle.end_fill()

    #right wing
    oval_turtle.penup()
    oval_turtle.goto(x_coords_list[z], y_coords_list[z]-50)
    oval_turtle.setheading(90)
    oval_turtle.pendown()
    oval_turtle.begin_fill()
    oval_turtle.forward(30)
    oval_turtle.right(115)
    oval_turtle.forward(80)
    oval_turtle.right(70)
    oval_turtle.forward(15)
    oval_turtle.right(95)
    oval_turtle.forward(80)
    oval_turtle.end_fill()

    #left wing
    oval_turtle.penup()
    oval_turtle.goto(x_coords_list[z], y_coords_list[0]-50)
    oval_turtle.right(80)
    oval_turtle.pendown()
    oval_turtle.begin_fill()
    oval_turtle.color("blue")
    oval_turtle.forward(30)
    oval_turtle.left(115)
    oval_turtle.forward(80)
    oval_turtle.left(70)
    oval_turtle.forward(15)
    oval_turtle.left(95)
    oval_turtle.forward(80)
    oval_turtle.end_fill()

    #tail left side
    oval_turtle.penup()
    oval_turtle.goto(x_coords_list[z], y_coords_list[0]-30)
    oval_turtle.left(85)
    oval_turtle.left(180)
    oval_turtle.color("blue")
    oval_turtle.forward(70)
    oval_turtle.right(58)
    oval_turtle.pendown()
    oval_turtle.begin_fill()
    oval_turtle.forward(50)
    oval_turtle.left(50)
    oval_turtle.forward(20)
    oval_turtle.left(120)
    oval_turtle.forward(55)
    oval_turtle.end_fill()

    # tail right side
    oval_turtle.penup()
    oval_turtle.goto(x_coords_list[z]-24, y_coords_list[0]-123)
    oval_turtle.right(30)
    oval_turtle.forward(20)
    oval_turtle.left(90)
    oval_turtle.forward(25)
    oval_turtle.right(125)
    oval_turtle.pendown()
    oval_turtle.begin_fill()
    oval_turtle.forward(50)
    oval_turtle.right(50)
    oval_turtle.forward(20)
    oval_turtle.right(122)
    oval_turtle.forward(65)
    oval_turtle.end_fill()

    # Hide the turtle after drawing the airplane
    oval_turtle.hideturtle()
    screen.update()

# Keep the window open
turtle.done()
