from sqlalchemy import select

from tim.models import Entry

def open_entries(session):

    # newest first
    #rows = session.execute(select(Entry).where(Entry.stop.is_(None)).order_by(Entry.start.desc()))
    
    # oldest first
    rows = session.execute(select(Entry).where(Entry.stop.is_(None)).order_by(Entry.start))
    return [x[0] for x in rows.all()]
