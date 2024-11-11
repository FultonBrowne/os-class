from libosclass import OSDateType

# Initialize an empty list to store the instances
data_list = []

# Generate ten instances with sample data
for i in range(10):
    fname = f'FirstName{i+1}'
    lname = f'LastName{i+1}'
    dob = f'01/{i+1:02d}/1990'  # Dates from 01/01/1990 to 01/10/1990
    phone = f'555-123-45{i+1:02d}'  # Phone numbers like 555-123-4501
    street_address = f'{100 + i} Main St'
    city = 'Anytown'
    state = 'State'
    zip_code = f'1234{i+1:02d}'  # Zip codes like 1234501
    # Create a new instance of OSDateType with the sample data
    os_data = OSDateType(fname, lname, dob, phone, street_address, city, state, zip_code)
    # Add the instance to the list
    data_list.append(os_data)

# creat a new file to store the data
with open('data.txt', 'w') as f:
    # Write the data from the instances to the file
    for os_data in data_list:
        f.write(f'{os_data.fname},{os_data.lname},{os_data.dob},{os_data.phone},{os_data.street_address},{os_data.city},{os_data.state},{os_data.zip}\n')
