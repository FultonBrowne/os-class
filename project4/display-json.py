from libosclass import OSDateType
from rich.console import Console
from rich.table import Table


import json
# read data from the file
data_to_show = []

table = Table(title="People")

table.add_column("First Name", style="cyan")
table.add_column("Last Name", style="magenta")
table.add_column("Date of Birth", style="green")
table.add_column("Phone", style="yellow")
table.add_column("Street Address", style="blue")
table.add_column("City", style="red")
table.add_column("State", style="cyan")
table.add_column("Zip", style="magenta")

with open('data.json', 'r') as f:
    data = json.load(f)

    for line in data:
        # get the data from the class and turn it in to a list of strings
        print(line.keys())
        fields = [line['fname'], line['lname'], line['dob'], line['phone'], line['street_address'], line['city'], line['state'], line['zip']]
        table.add_row(*fields, style='bright_green')
    console = Console()
    console.print(table)
