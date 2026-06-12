from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Deal(db.Model):
    __tablename__ = "deals"

    id = db.Column(db.String(36), primary_key=True)
    destination = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    platform = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.Float, nullable=False)
    travel_type = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "destination": self.destination,
            "price": self.price,
            "platform": self.platform,
            "rating": self.rating,
            "travel_type": self.travel_type,
            "created_at": self.created_at.isoformat() + "Z",
        }


def get_all_deals():
    return [deal.to_dict() for deal in Deal.query.all()]


def get_deal_by_id(deal_id):
    deal = Deal.query.get(deal_id)
    return deal.to_dict() if deal else None


def insert_deal(data):
    import uuid
    deal = Deal(
        id=str(uuid.uuid4()),
        destination=data["destination"],
        price=data["price"],
        platform=data["platform"],
        rating=data["rating"],
        travel_type=data["travel_type"],
    )
    db.session.add(deal)
    db.session.commit()
    return deal.to_dict()