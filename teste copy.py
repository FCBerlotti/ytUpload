from datetime import date, datetime

startDate = (date.today()).day 
futureDate = datetime.strptime("27/07/2025", "%d/%m/%Y").date()

print(futureDate.day)