from database import SessionLocal
from models import Agent

agents = [
    {
        "name": "Shipping Agent",
        "email": "shipping@sage.com",
        "phone": "+911111111111",
        "category": "Shipping"
    }
]

db = SessionLocal()

for a in agents:

    exists = db.query(Agent).filter(
        Agent.email == a["email"]
    ).first()

    if not exists:
        db.add(Agent(**a))

db.commit()

print("Agents seeded")