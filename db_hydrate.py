from faker import Factory
from models import Customer, app, db

db.create_all(app=app)

l = []
for customer in range(0, 10):
    fake = Factory.create('fr_FR')
    n = fake.name()
    c = fake.company()
    e = fake.email()
    l.append([n, c, e])
    nu_add = Customer(name=n,
                      company=c,
                      email=e)
    db.session.add(nu_add)
    db.session.commit()

for i in l:
    print(i)
