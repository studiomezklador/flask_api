from models import Customer

customers = Customer.query.all()

print(customers)
