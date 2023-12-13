from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models import Base


class ClientDiagnosis(Base):
    __tablename__ = 'client_diagnosis'

    diagnosis_id: Mapped[int] = mapped_column(
        ForeignKey('diagnosis.id', ondelete='CASCADE'), index=True
    )
    client_id: Mapped[int] = mapped_column(
        ForeignKey('client.id', ondelete='CASCADE'), index=True
    )
    doctor_id: Mapped[int] = mapped_column(
        ForeignKey('doctor.id', ondelete='CASCADE'), index=True
    )

    diagnosis: Mapped['Diagnosis'] = relationship(
        back_populates='client_diagnosis'
    )
    client: Mapped['Client'] = relationship(back_populates='client_diagnosis')
    doctor: Mapped['Doctor'] = relationship(back_populates='client_diagnosis')
