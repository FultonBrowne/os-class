from libosclass import OSDateType
import json

# Initialize an empty list to store the instances
data_list = []

# Generate ten instances with sample data
for i in range(10):
    fname = ["John", "Sophia", "Michael", "Emily", "David", "Olivia", "Daniel", "Ava", "James", "Isabella"][i]
    lname = ["Doe", "Taylor", "Williams", "Martinez", "Clark", "Hernandez", "Lopez", "Garcia", "Anderson", "Lee"][i]
    dob = [
        "1985-07-20", "1992-03-14", "1978-11-03", "2000-06-25", "1980-01-10",
        "1995-09-17", "1988-04-05", "1999-12-12", "1990-08-30", "1993-02-22"
    ][i]
    phone = [
        "555-987-1234", "555-654-7890", "555-321-4567", "555-765-4321", "555-876-5432",
        "555-234-5678", "555-345-6789", "555-456-7890", "555-567-8901", "555-678-9012"
    ][i]
    street_address = [
        "1 Elm St", "202 Cherry Ln", "14 Maple Ave", "50 Pine Rd", "303 Spruce Ct",
        "88 Cedar Blvd", "6 Birch Dr", "99 Oak Cir", "75 Walnut St", "200 Ash Ave"
    ][i]
    city = [
        "Austin", "Denver", "Seattle", "Miami", "Chicago",
        "Phoenix", "Boston", "Nashville", "San Diego", "Portland"
    ][i]
    state = ["TX", "CO", "WA", "FL", "IL", "AZ", "MA", "TN", "CA", "OR"][i]
    zip_code = [
        "73301", "80202", "98101", "33101", "60601",
        "85001", "02108", "37201", "92101", "97201"
    ][i]

    # Create a new instance of OSDateType with the sample data
    os_data = OSDateType(fname, lname, dob, phone, street_address, city, state, zip_code)
    # Add the instance to the list
    data_list.append(os_data)

# creat a new file to store the data
with open('data.json', 'w') as f:
    f.write(json.dumps([os_data.__dict__ for os_data in data_list], indent=4))
