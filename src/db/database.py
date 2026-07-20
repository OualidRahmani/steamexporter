# database.py
from datetime import datetime
from typing import Optional

from sqlalchemy import String, Float, Integer, DateTime, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker

from src.core.models import Game

# 1. Define the Base class for the ORM
class Base(DeclarativeBase):
    pass

# 2. Define the Table Schema as a Python Class
class DBGame(Base):
    __tablename__ = "games"

    appid: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    playtime_hours: Mapped[float] = mapped_column(Float, default=0.0)
    last_played: Mapped[Optional[datetime]] = mapped_column(DateTime)
    release_date: Mapped[Optional[str]] = mapped_column(String)
    
    # We store lists as comma-separated strings in SQLite
    developers: Mapped[Optional[str]] = mapped_column(String)
    publishers: Mapped[Optional[str]] = mapped_column(String)
    
    price: Mapped[Optional[str]] = mapped_column(String)
    discount: Mapped[Optional[int]] = mapped_column(Integer)

# 3. Setup the Engine and Session
# "sqlite:///library.db" creates a local file named library.db in your root folder.
engine = create_engine("sqlite:///library.db", echo=False) 

# Create the tables in the database if they don't exist yet
Base.metadata.create_all(engine)

# Create a factory for generating new database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def save_games_to_db(games: list[Game]):
    """Injects or updates the library data into the SQLite database."""
    session = SessionLocal()
    
    try:
        for game in games:
            # Map the Python dataclass to the SQLAlchemy ORM model
            db_game = DBGame(
                appid=game.appid,
                name=game.name,
                playtime_hours=round(game.playtime_hours, 1),
                last_played=game.last_played,
                release_date=game.release_date,
                developers=", ".join(game.developers) if game.developers else None,
                publishers=", ".join(game.publishers) if game.publishers else None,
                price=game.price,
                discount=game.discount
            )
            # session.merge() acts as an "upsert". 
            # If the appid already exists, it updates the row. If not, it inserts it.
            session.merge(db_game)
            
        # Commit the transaction to save the changes to disk
        session.commit()
    except Exception as e:
        # If anything goes wrong, rollback the transaction so we don't corrupt the DB
        session.rollback()
        print(f"Database error: {e}")
    finally:
        # Always close the session
        session.close()