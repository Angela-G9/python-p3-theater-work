from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

# Database setup
DATABASE_URL = 'sqlite:///moringa_theater.db'
engine = create_engine(DATABASE_URL)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

# Define Models
class Role(Base):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True)
    character_name = Column(String, nullable=False)

    auditions = relationship("Audition", back_populates="role", cascade="all, delete")
    
    def actors(self):
        return [audition.actor for audition in self.auditions]
    
    def locations(self):
        return [audition.location for audition in self.auditions]
    
    def lead(self):
        hired_auditions = [audition for audition in self.auditions if audition.hired]
        return hired_auditions[0] if hired_auditions else "No actor has been hired for this role"
    
    def understudy(self):
        hired_auditions = [audition for audition in self.auditions if audition.hired]
        return hired_auditions[1] if len(hired_auditions) > 1 else "No actor has been hired for understudy for this role"

class Audition(Base):
    __tablename__ = 'auditions'
    id = Column(Integer, primary_key=True)
    actor = Column(String, nullable=False)
    location = Column(String, nullable=False)
    phone = Column(Integer, nullable=False)
    hired = Column(Boolean, default=False)
    role_id = Column(Integer, ForeignKey('roles.id'))

    role = relationship("Role", back_populates="auditions")
    
    def call_back(self):
        self.hired = True
        session.commit()

# Create tables
Base.metadata.create_all(engine)

# CRUD Operations

def create_role(character_name):
    role = Role(character_name=character_name)
    session.add(role)
    session.commit()
    return role

def create_audition(actor, location, phone, role_id):
    audition = Audition(actor=actor, location=location, phone=phone, role_id=role_id)
    session.add(audition)
    session.commit()
    return audition

def get_roles():
    return session.query(Role).all()

def get_auditions():
    return session.query(Audition).all()

if __name__ == "__main__":
    role = create_role("Role")
    audition1 = create_audition("charactername", "place", 123456789, role.id)
    
    
    print(f"Role: {role.character_name}, Actors: {role.actors()}")
