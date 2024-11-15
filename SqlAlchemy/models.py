from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


class Base(DeclarativeBase):
	pass


class UserBase(Base):
	__tablename__ = "user_telegramm"

	id: Mapped[int] = mapped_column(primary_key=True)
	name: Mapped[str] = mapped_column(String(50))
	chat_id: Mapped[int] = mapped_column()
	notification: Mapped[bool] = mapped_column(default=True)

	def __repr__(self):
		return f"ID: {self.id} | Name: {self.name} | Chat_id: {self.chat_id} | Notification: {self.notification}"

