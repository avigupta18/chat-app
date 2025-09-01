from .models import Message
from .db import async_session

async def save_message(room_id: int, sender: str, content: str):
    async with async_session() as session:
        msg = Message(room_id=room_id, sender=sender, content=content)
        session.add(msg)
        await session.commit()
        await session.refresh(msg)
        return msg
