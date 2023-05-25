import pandas as pd
from sqlalchemy.exc import IntegrityError

from app.database import get_db
from app.models import Location

df = pd.read_csv('uszips.csv')

df = df[['zip', 'lat', 'lng', 'city', 'state_id']]

df = df.head(100)

data = df.to_dict('records')

async with get_db() as session:

    for row in data:

        location = Location(
            city=row['city'],
            state=row['state_id'],
            zip_code=row['zip'],
            latitude=row['lat'],
            longitude=row['lng'],
        )

        try:
            session.add(location)
            await session.flush()
        except IntegrityError:
            session.rollback()
            print(f"Location {location.zip_code} already exists in the database. Skipping...")

    await session.commit()
