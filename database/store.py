import uuid
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# In-memory list to track recently viewed deal IDs (last 10)
_recently_viewed = []
MAX_RECENT = 10


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


# ---------------- Basic CRUD ------------------------

def get_all_deals():
    return [deal.to_dict() for deal in Deal.query.all()]


def get_deal_by_id(deal_id):
    deal = db.session.get(Deal, deal_id)
    if deal:
        _track_recent(deal_id)
    return deal.to_dict() if deal else None


def insert_deal(data):
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


# ---------------- Search ------------------------

def search_deals(destination=None, platform=None, travel_type=None):
    query = Deal.query

    if destination:
        query = query.filter(Deal.destination.ilike(f"%{destination}%"))

    if platform:
        query = query.filter(Deal.platform.ilike(f"%{platform}%"))

    if travel_type:
        query = query.filter(Deal.travel_type.ilike(f"%{travel_type}%"))

    return [deal.to_dict() for deal in query.all()]


# ---------------- Filter ------------------------

def filter_deals_by_price(min_price=None, max_price=None):
    query = Deal.query

    if min_price is not None:
        query = query.filter(Deal.price >= float(min_price))

    if max_price is not None:
        query = query.filter(Deal.price <= float(max_price))

    return [deal.to_dict() for deal in query.all()]


# ---------------- Sort ------------------------

def sort_deals(sort_by="price", order="asc"):
    column = getattr(Deal, sort_by, Deal.price)
    if order.lower() == "desc":
        column = column.desc()
    return [deal.to_dict() for deal in Deal.query.order_by(column).all()]


# ---------------- Recently Viewed ------------------

def _track_recent(deal_id):
    if deal_id in _recently_viewed:
        _recently_viewed.remove(deal_id)
    _recently_viewed.insert(0, deal_id)
    if len(_recently_viewed) > MAX_RECENT:
        _recently_viewed.pop()


def get_recently_viewed():
    deals = []
    for deal_id in _recently_viewed:
        deal = db.session.get(Deal, deal_id)
        if deal:
            deals.append(deal.to_dict())
    return deals