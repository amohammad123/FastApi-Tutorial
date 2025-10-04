from datetime import datetime

from sqlalchemy import create_engine, Column, Integer, String, Boolean, or_, and_, not_, func, ForeignKey, Text, \
    DateTime
from sqlalchemy.orm import sessionmaker, declarative_base, relationship, backref

SQLALCHEMY_DATABASE_URI = 'sqlite:///./sqlite.db'

engine = create_engine(
    SQLALCHEMY_DATABASE_URI,
    connect_args={"check_same_thread": False},
    echo=True
)
sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(30))
    last_name = Column(String(30), nullable=True)
    age = Column(Integer)
    is_active = Column(Boolean)
    is_verify = Column(Boolean)

    # addresses = relationship('Address', back_populates="User")
    addresses = relationship('Address', backref="User")


    def __repr__(self):
        return f'User(id={self.id}, first_name={self.first_name}, last_name={self.last_name})'


class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, autoincrement=True)
    total_amount = Column(Integer)

class Address(Base):
    __tablename__ = 'addresses'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    city = Column(String(30))

    # user = relationship('User', back_populates="addresses")


class Profile(Base):
    __tablename__ = 'profiles'

    id = Column(Integer, primary_key=True, autoincrement=True)
    bio = Column(Text)
    user_id = Column(Integer, ForeignKey('users.id'), unique=True, uselist=False)

class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True, autoincrement=True)
    create_date = Column(DateTime(), default=datetime.now)
    update_date = Column(DateTime(), default=datetime.now, onupdate=datetime.now)
    parent_id = Column(Integer, ForeignKey('categories.id'), nullable=True)
    title = Column(Text)

    # parent = relationship('Category', back_populates='children', remote_side=[id])
    # children = relationship('Category', back_populates='parent', remote_side=[parent_id])
    children = relationship('Category', backref=backref("parent", remote_side=[id]))


Base.metadata.create_all(engine)

session = sessionLocal()

# create
create_user = User(first_name='ali', age=11)
session.add(create_user)
session.commit()

# bulk create
maryam = User(first_name='maryam', age=22)
ahmad = User(first_name='ahmad', age=23)
users = [maryam, ahmad]
session.add_all(users)
session.commit()

# retrieve all data
get_users = session.query(User).all()
print(get_users)

# retrieve data with filter
get_user_by_filter = session.query(User).filter_by(age=10, first_name='ali').all()
print(get_user_by_filter)

# update
update_user = session.query(User).filter_by(age=10, first_name='ali').all()
update_user.last_name = 'ahmadi'
session.commit()

# delete
delete_user = session.query(User).filter_by(age=10, first_name='ali').all()
session.delete(delete_user)
session.commit()

# complex query
complex_query = session.query(User).filter(User.age >= 10, User.first_name == 'ali').all()
complex_query2 = session.query(User).where(User.age >= 10, User.first_name == 'ali').all()
complex_query3 = session.query(User).filter(User.age >= 10, User.first_name.like("%ali%")).all()  # key sensitive
complex_query4 = session.query(User).filter(User.age >= 10, User.first_name.ilike("%ali%")).all()

complex_query5 = session.query(User).filter(or_(User.age >= 10, User.first_name.ilike("%ali%"))).all()
complex_query6 = session.query(User).filter(and_(User.age >= 10, User.first_name.ilike("%ali%"))).all()
complex_query7 = session.query(User).filter(not_(User.first_name.ilike("%ali%"))).all()
complex_query8 = session.query(User).filter(or_(not_(User.first_name == 'ali'), and_(User.age > 30))).all()

total_users = session.query(func.count(User.id)).scalar()  # return just a number
avg_user_age = session.query(func.avg(User.age)).scalar()

annotation = session.query(
    User.first_name, func.sum(Order.total_amount).label("total_spent")
).join(Order).group_by(User.id).order_by(func.sum(Order.total_amount).desc()).limit(5).all()


# relation
relation = session.query(User).filter_by(first_name='ali').one_or_none()
addresses = [Address(user_id=relation.id, city="tehran"), Address(user_id=relation.id, city="rasht")]
session.add_all(addresses)
session.commit()

address = session.query(Address).filter_by(user_id=relation.id, city='rasht').one_or_none()
user_address = address.user.first_name


