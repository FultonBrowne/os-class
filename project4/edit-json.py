from libosclass import OSDateType
import json

# Initialize an empty list to store the instances
data_list = []

# Generate ten instances with sample data
for i in range(5):
    fname = ["Alice", "Bob", "Charlie", "Diana", "Edward"][i]
    lname = ["Smith", "Johnson", "Brown", "Davis", "Miller"][i]
    dob = f'1990-0{i+1}-15'  # Birthdates spread out through the first 5 months of 1990
    phone = f'555-456-{7000 + i}'  # Phone numbers like 555-456-7000
    street_address = [f'101 Oak St', f'202 Maple Ave', f'303 Pine Dr', f'404 Birch Ln', f'505 Cedar Ct'][i]
    city = ["Springfield", "Riverside", "Fairview", "Greenville", "Madison"][i]
    state = ["CA", "NY", "TX", "FL", "WA"][i]
    zip_code = f'{90001 + i}'  # Zip codes like 90001, 90002, ...

    # Create a new instance of OSDateType with the sample data
    os_data = OSDateType(fname, lname, dob, phone, street_address, city, state, zip_code)
    # Add the instance to the list
    data_list.append(os_data)

    f = open('data.json', 'r')
    data = json.load(f)
    f.close()
    f = open('data.json', 'w')
    for i in data_list:
        data.append(i.__dict__)
    f.write(json.dumps(data, indent=4))
