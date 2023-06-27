from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.orm import sessionmaker



engine = create_engine('postgresql://user:password@localhost:5432/task2')


Session = sessionmaker(bind=engine)

session = Session()

Base = declarative_base()

class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    user_type = Column(String)
    

class Host(Base):
    __tablename__ = 'host'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))


class Guest(Base):
    __tablename__ = 'guest'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    possibility = Column(String) 


class Reservation(Base):
    __tablename__ = 'reservation'

    id = Column(Integer, primary_key=True)
    guest_id = Column(Integer, ForeignKey('guest.id'))
    free_room_id = Column(Integer)
    from_time = Column(String)
    to_time = Column(String)


class Rooms(Base):
    __tablename__ = 'rooms'

    id = Column(Integer, primary_key=True)
    host_id = Column(Integer, ForeignKey('host.id'))
    room_name = Column(String)
    attributes = Column(String)
    price = Column(Integer)
    status = Column(String)
    from_time = Column(String)
    to_time = Column(String)


class FreeRooms(Base):
    __tablename__ = 'free_rooms'

    id = Column(Integer, primary_key=True)
    room_id = Column(Integer, ForeignKey('rooms.id'))


class Availability(Base):
    __tablename__ = 'availability'

    id = Column(Integer, primary_key=True)
    guest_id = Column(Integer, ForeignKey('guest.id'))
    free_room_id = Column(Integer, ForeignKey('free_rooms.id'))

Base.metadata.create_all(engine)



name_host = ['John','Sandra','Lilly']
name_guest = ['Kate', 'Alex', 'Brad']
for q in name_host:
    new_host = Users(name = q, user_type = 'host')
    session.add(new_host)

session.commit()



for q in name_guest:
    new_guest = Users(name = q, user_type = 'guest')
    session.add(new_guest)

session.commit()


all_guest_users = session.query(Users).filter(Users.user_type=='guest').all()
for users in all_guest_users:
    guest = Guest(user_id = users.id, possibility = 'reservation')
    session.add(guest)

session.commit()


all_host_users = session.query(Users).filter(Users.user_type=='host').all()
for users in all_guest_users:
    host = Host(user_id = users.id)
    session.add(host)

session.commit()



room = Rooms(host_id = 1, attributes = 'A', price = 100, status = 'Free', from_time = None, to_time = None)
session.add(room)
room = Rooms(host_id = 2, attributes = 'A, B', price = 500, status = 'Free', from_time = None, to_time = None)
session.add(room)
room = Rooms(host_id = 3, attributes = 'A, B, C', price = 1200, status = 'Free', from_time = None, to_time = None)
session.add(room)
session.commit()


all_free_rooms = session.query(Rooms).filter(Rooms.status=='Free').all()
for room in all_free_rooms:
    free_room = FreeRooms(room_id = room.id)
    session.add(free_room)

session.commit()


reservation = Reservation(guest_id = 1, free_room_id = 1, from_time='25.06.2023', to_time = '27.06.2023')
session.add(reservation)
reservation = Reservation(guest_id = 2, free_room_id = 2, from_time='25.06.2023', to_time = '28.06.2023')
session.add(reservation)
reservation = Reservation(guest_id = 3, free_room_id = 3, from_time='25.06.2023', to_time = '30.06.2023')
session.add(reservation)

session.commit()

changing_status = session.query(Reservation).all()
for status in changing_status:
    rooms = session.query(Rooms).all()
    for room in rooms:
        if room.id == status.free_room_id:
            room.status = 'Occupied'
            room.from_time = status.from_time
            room.to_time = status.to_time
        session.commit()

semi_result = session.query(Guest,Reservation).join(Reservation).all()
result = session.query(Users).all()
for q in result:
    for guest,reservation in semi_result:
        if q.id == guest.user_id:
            res = session.query(Users).filter(Users.id == q.id).first()
            print(res.name, res.id)
