from sqlalchemy import Column, Date, ForeignKeyConstraint, Identity, Integer, LargeBinary, PrimaryKeyConstraint, String, \
    Table, Text, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from app_config import db



Base = declarative_base()
metadata = Base.metadata


class User(Base):
    __tablename__ = 'User'
    __table_args__ = (
        PrimaryKeyConstraint('user_id', name='User_pkey'),
    )

    user_id = Column(Integer, Identity(always=True, start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1))
    login = Column(String(20))
    password = Column(String(30))

    event = relationship('Event', back_populates='user')

    # Flask-Login Support
    def is_active(self):
        """True, as all users are active."""

        return True

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""

        return str(self.user_id)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False

#    def __repr__(self):
#        return '<User %r>' % self.user_id


class Type(Base):
    __tablename__ = 'type'
    __table_args__ = (
        PrimaryKeyConstraint('type_id', name='Topic_pkey'),
    )

    type_id = Column(Integer, Identity(always=True, start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1))
    name = Column(Text)

    event = relationship('Event', secondary='event_type', back_populates='type')


class Event(Base):
    __tablename__ = 'event'
    __table_args__ = (
        ForeignKeyConstraint(['user_id'], ['User.user_id'], name='FK_user_id'),
        PrimaryKeyConstraint('event_id', name='Event_pkey')
    )

    event_id = Column(Integer, Identity(always=True, start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1))
    date = Column(Date, nullable=False)
    title = Column(Text, nullable=False)
    user_id = Column(ForeignKey('User.user_id'), nullable=False)
    comment = Column(Text)

    user = relationship('User', back_populates='event')
    type = relationship('Type', secondary='event_type', back_populates='event')
    photo = relationship('Photo', back_populates='event')


t_event_type = Table(
    'event_type', metadata,
    Column('event_id', ForeignKey('event.event_id'), nullable=False),
    Column('type_id', ForeignKey('type.type_id'), nullable=False),
    ForeignKeyConstraint(['event_id'], ['event.event_id'], name='FK_event_id'),
    ForeignKeyConstraint(['type_id'], ['type.type_id'], name='FK_topic_id'),
    PrimaryKeyConstraint('event_id', 'type_id', name='event_topic_pkey')
)


class Photo(Base):
    __tablename__ = 'photo'
    __table_args__ = (
        ForeignKeyConstraint(['event_id'], ['event.event_id'], name='FK_event_id'),
        PrimaryKeyConstraint('photo_id', name='Photo_pkey')
    )

    photo_id = Column(Integer, Identity(always=True, start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1))
    event_id = Column(ForeignKey('event.event_id'))
    photography = Column(LargeBinary)

    event = relationship('Event', back_populates='photo')
