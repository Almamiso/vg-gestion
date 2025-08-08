from sqlalchemy import BigInteger, Integer, String, Date, DateTime, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from app.db.base import Base

class ManufacturingOrder(Base):
    __tablename__ = "manufacturing_orders"

    mo_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    location_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("locations.location_id"))
    status: Mapped[str | None] = mapped_column(String, nullable=True)
    due_date: Mapped[str | None] = mapped_column(Date, nullable=True)
    start_time: Mapped[str | None] = mapped_column(DateTime(timezone=True), nullable=True)
    end_time: Mapped[str | None] = mapped_column(DateTime(timezone=True), nullable=True)
    total_duration: Mapped[int | None] = mapped_column(Integer, nullable=True)
    total_cost: Mapped[float | None] = mapped_column(Numeric(12,4), nullable=True)
    created_by: Mapped[str | None] = mapped_column(String, nullable=True)

class MOProduct(Base):
    __tablename__ = "mo_produits"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    mo_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("manufacturing_orders.mo_id", ondelete="CASCADE"))
    produit_id: Mapped[int] = mapped_column(Integer, ForeignKey("produits.produit_id"))
    qty_to_build: Mapped[float] = mapped_column(Numeric(12,4))
    qty_done: Mapped[float | None] = mapped_column(Numeric(12,4), default=0)
    avg_build_time: Mapped[int | None] = mapped_column(Integer, nullable=True)

class MOComponent(Base):
    __tablename__ = "mo_composants"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    mo_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("manufacturing_orders.mo_id", ondelete="CASCADE"))
    type_composant: Mapped[str] = mapped_column(String)
    composant_id: Mapped[int] = mapped_column(Integer)
    qty_required: Mapped[float] = mapped_column(Numeric(12,4))
    qty_issued: Mapped[float | None] = mapped_column(Numeric(12,4), default=0)

class WorkCenter(Base):
    __tablename__ = "work_centers"

    wc_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nom: Mapped[str] = mapped_column(String, nullable=False)
    location_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("locations.location_id"))
    capacite_h_j: Mapped[float | None] = mapped_column(Numeric(6,2), nullable=True)
    taux_horaire: Mapped[float | None] = mapped_column(Numeric(12,4), nullable=True)
    actif: Mapped[bool | None] = mapped_column(Integer, default=True)

class Routing(Base):
    __tablename__ = "routings"

    routing_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    produit_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("produits.produit_id"))
    version: Mapped[str | None] = mapped_column(String, nullable=True)
    actif: Mapped[bool | None] = mapped_column(Integer, default=True)

class RoutingStep(Base):
    __tablename__ = "routing_steps"

    step_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    routing_id: Mapped[int] = mapped_column(Integer, ForeignKey("routings.routing_id", ondelete="CASCADE"))
    ordre: Mapped[int | None] = mapped_column(Integer, nullable=True)
    wc_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("work_centers.wc_id"))
    label: Mapped[str | None] = mapped_column(String, nullable=True)
    temps_std_min: Mapped[int | None] = mapped_column(Integer, nullable=True)
    setup_std_min: Mapped[int | None] = mapped_column(Integer, nullable=True)

class MOOperation(Base):
    __tablename__ = "mo_operations"

    mo_op_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    mo_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("manufacturing_orders.mo_id", ondelete="CASCADE"))
    step_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("routing_steps.step_id"))
    status: Mapped[str | None] = mapped_column(String, nullable=True)
    start_at: Mapped[str | None] = mapped_column(DateTime(timezone=True), nullable=True)
    end_at: Mapped[str | None] = mapped_column(DateTime(timezone=True), nullable=True)
    duree_min: Mapped[int | None] = mapped_column(Integer, nullable=True)

class MOTimelog(Base):
    __tablename__ = "mo_timelogs"

    log_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    mo_op_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("mo_operations.mo_op_id", ondelete="CASCADE"))
    user_id: Mapped[str | None] = mapped_column(String, nullable=True)
    started_at: Mapped[str | None] = mapped_column(DateTime(timezone=True), server_default=func.now())
    ended_at: Mapped[str | None] = mapped_column(DateTime(timezone=True), nullable=True)
    minutes: Mapped[int | None] = mapped_column(Integer, nullable=True)