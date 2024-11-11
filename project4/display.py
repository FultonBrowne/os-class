from libosclass import OSDateType
from rich.console import Console
from rich.table import Table
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

with open('data.txt', 'r') as f:
    for line in f:
        # Split the line into fields
        fields = line.strip().split(',')
        table.add_row(*fields, style='bright_green')
    console = Console()
    console.print(table)
