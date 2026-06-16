import uuid
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# In-memory list to track recently viewed deal IDs (last 10)
_recently_viewed = []
MAX_RECENT = 10


class Deal(db.Model):
    __tablename__ = "deals"

    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    destination = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    platform = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.Float, nullable=False)
    travel_type = db.Column(db.String(50), nullable=False)
    view_count = db.Column(db.Integer, default=0, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "destination": self.destination,
            "price": self.price,
            "platform": self.platform,
            "rating": self.rating,
            "travel_type": self.travel_type,
            "view_count": self.view_count,
            "created_at": self.created_at.isoformat() + "Z",
            "updated_at": self.updated_at.isoformat() + "Z" if self.updated_at else None,
        }


class SearchStat(db.Model):
    __tablename__ = "search_stats"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    destination = db.Column(db.String(100), unique=False, nullable=True)
    search_count = db.Column(db.Integer, default=0, nullable=False)



class ApiStat(db.Model):
    __tablename__ = "api_stats"

    id = db.Column(db.Integer, primary_key=True)
    total_requests = db.Column(db.Integer, default=0, nullable=False)
    successful_requests = db.Column(db.Integer, default=0, nullable=False)
    failed_requests = db.Column(db.Integer, default=0, nullable=False)

# ---------------- Basic CRUD ------------------------

def get_all_deals():
    return [deal.to_dict() for deal in Deal.query.all()]


def get_deal_by_id(deal_id):
    deal = db.session.get(Deal, deal_id)
    if deal:
        deal.view_count = (deal.view_count or 0) + 1
        db.session.commit()
        _track_recent(deal_id)
        return deal.to_dict()
    return None


def insert_deal(data):
    deal = Deal(
        # id=str(uuid.uuid4()),
        destination=data["destination"],
        price=data["price"],
        platform=data["platform"],
        rating=data["rating"],
        travel_type=data["travel_type"],
    )
    db.session.add(deal)
    db.session.commit()
    return deal.to_dict()



#-----------------------Update---------------------

def update_deal(deal_id, data):
    deal = db.session.get(Deal, deal_id)
    if not deal:
        return None

    deal.destination = data["destination"]
    deal.price = data["price"]
    deal.platform = data["platform"]
    deal.rating = data["rating"]
    deal.travel_type = data["travel_type"]

    db.session.commit()
    return deal.to_dict()



#-----------------------Delete---------------------

def delete_deal(deal_id):
    deal = db.session.get(Deal, deal_id)
    if not deal:
        return False

    db.session.delete(deal)
    db.session.commit()

    if deal_id in _recently_viewed:
        _recently_viewed.remove(deal_id)

    return True


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





# ---------------- Popular Deals ------------------

def get_popular_deals(limit=10):
    deals = (
        Deal.query.order_by(Deal.view_count.desc(), Deal.created_at.desc())
        .limit(limit)
        .all()
    )
    return [deal.to_dict() for deal in deals]


def get_most_viewed_deal():
    deal = Deal.query.order_by(Deal.view_count.desc()).first()
    if not deal or deal.view_count == 0:
        return None
    return deal.to_dict()


# ---------------- Search Stats ------------------

def record_search_term(destination):
    key = destination.strip().lower()
    if not key:
        return

    stat = SearchStat.query.filter_by(destination=key).first()
    if stat:
        stat.search_count += 1
    else:
        stat = SearchStat(destination=key, search_count=1)
        db.session.add(stat)
    db.session.commit()


def get_most_searched_destination():
    stat = SearchStat.query.order_by(SearchStat.search_count.desc()).first()
    if not stat:
        return None
    return {"destination": stat.destination.title(), "search_count": stat.search_count}


# ---------------- API Usage Stats ------------------

def _get_or_create_api_stat():
    stat = db.session.get(ApiStat, 1)
    if not stat:
        stat = ApiStat(id=1, total_requests=0, successful_requests=0, failed_requests=0)
        db.session.add(stat)
        db.session.commit()
    return stat


def record_api_request(success):
    stat = _get_or_create_api_stat()
    stat.total_requests += 1
    if success:
        stat.successful_requests += 1
    else:
        stat.failed_requests += 1
    db.session.commit()


def get_api_usage_stats():
    stat = _get_or_create_api_stat()
    return {
        "total_requests": stat.total_requests,
        "successful_requests": stat.successful_requests,
        "failed_requests": stat.failed_requests,
        "most_searched_destination": get_most_searched_destination(),
        "most_viewed_deal": get_most_viewed_deal(),
    }