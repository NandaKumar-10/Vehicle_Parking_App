from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import *
from sqlalchemy.orm import Mapped, mapped_column, relationship,join
import bcrypt

db=SQLAlchemy()

class Admin(db.Model):
    __tablename__ = "Admin"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(300), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    password: Mapped[str] = mapped_column(String(300), nullable=False)

    def __init__(self,email,name,password):
        self.name=name
        self.email=email
        self.password=bcrypt.hashpw(password.encode('UTF-8'),bcrypt.gensalt()).decode('UTF-8')
    
    def check_password(self,password):
        return bcrypt.checkpw(password.encode('UTF-8'), self.password.encode('UTF-8'))

class User(db.Model):
    __tablename__ = "User"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    password: Mapped[str] = mapped_column(String(100), nullable=False)
    address: Mapped[str] = mapped_column(String(200), nullable=False)
    pincode: Mapped[str] = mapped_column(String(50), nullable=False)

    def __init__(self,email,name,password,address,pincode):
        self.name=name
        self.email=email
        self.password=bcrypt.hashpw(password.encode('UTF-8'), bcrypt.gensalt()).decode('UTF-8')
        self.address=address
        self.pincode=pincode

    def check_password(self,password):
        return bcrypt.checkpw(password.encode('UTF-8'), self.password.encode('UTF-8'))

    def set_password(self,password):
        return bcrypt.hashpw(password.encode('UTF-8'), bcrypt.gensalt()).decode('UTF-8')

class Parking_Lot(db.Model):
    __tablename__ = "Parking_Lot"
    id: Mapped[int] = mapped_column(primary_key=True)
    city:Mapped[str] = mapped_column(String(100),nullable=False)
    prime_location_name: Mapped[str] = mapped_column(String(100),nullable=False)
    price: Mapped[int] = mapped_column(nullable=False)
    address: Mapped[str] = mapped_column(String(200),nullable=False)
    pincode: Mapped[str] = mapped_column(String(50),nullable=False)
    max_no_spots: Mapped[int] = mapped_column(nullable=False)
    no_spot_occupied: Mapped[int] = mapped_column(default=0)

    #spot=relationship('Parking_Spot',backref='lots',cascade='all, delete',lazy=True)
    spots = relationship("Parking_Spot", back_populates='lot',cascade='all, delete',lazy=True)

    def __init__(self,city,prime_location_name,price,address,pincode,max_no_spots):
        self.city=city
        self.prime_location_name=prime_location_name
        self.price=price
        self.address=address
        self.pincode=pincode
        self.max_no_spots=max_no_spots


class Parking_Spot(db.Model):
    __tablename__ = "Parking_Spot"

    id: Mapped[int] = mapped_column(primary_key=True)
    lot_id: Mapped[int] = mapped_column(ForeignKey("Parking_Lot.id",ondelete="CASCADE"))
    status: Mapped[str] = mapped_column(String(10),nullable=False)

    lot = relationship("Parking_Lot", back_populates="spots")
    reservations = relationship("Reserve_Parking_Spot", back_populates="spot", cascade="all, delete")
    def __init__(self,lot_id,status):
        self.lot_id=lot_id
        self.status=status

class Reserve_Parking_Spot(db.Model):
    __tablename__ = "Reserve_parking_spot"

    id: Mapped[int] = mapped_column(primary_key=True)
    spot_id: Mapped[int] = mapped_column(ForeignKey('Parking_Spot.id',ondelete='CASCADE'),nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey('User.id'))
    Parking_timestamp: Mapped[datetime] = mapped_column(DateTime,nullable=False)
    Leaving_timestamp: Mapped[datetime] = mapped_column(DateTime,nullable=True)
    parking_cost: Mapped[int] = mapped_column(nullable=True)
    vehicle_no: Mapped[str] = mapped_column(nullable=False)
    occupancy: Mapped[str] = mapped_column(default="Occupied")
    #status: Mapped[str] = mapped_column(ForeignKey('Parking_Spot.status'))

    #spot = relationship("Parking_Spot", back_populates="reservations", foreign_keys=[spot_id])
    spot = relationship("Parking_Spot", back_populates="reservations",passive_deletes=True)
    def __init__(self,spot_id,user_id,parking_timestamp,vehicle_no):
        self.spot_id=spot_id
        self.user_id=user_id
        self.Parking_timestamp=parking_timestamp
        self.vehicle_no=vehicle_no
        #self.status=status

class Booking_records(db.Model):
    __tablename__ = "BookingRecords"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('User.id'))
    lot_id: Mapped[int] = mapped_column(ForeignKey('Parking_Lot.id'))
    spot_id: Mapped[int] = mapped_column(ForeignKey('Parking_Spot.id'))
    location_name: Mapped[str] = mapped_column(ForeignKey('Parking_Lot.prime_location_name'))
    price: Mapped[int] = mapped_column(nullable=True)
    parking_timestamp: Mapped[datetime] = mapped_column(DateTime,nullable=False)
    leaving_timestamp: Mapped[datetime] = mapped_column(DateTime,nullable=True)
    vehicle_no: Mapped[str] = mapped_column(nullable=False)

    def __init__(self,user_id,lot_id,spot_id,parking_timestamp,vehicle_no,location_name):
        self.user_id = user_id
        self.lot_id = lot_id
        self.spot_id = spot_id
        self.parking_timestamp = parking_timestamp
        self.vehicle_no = vehicle_no
        self.location_name = location_name