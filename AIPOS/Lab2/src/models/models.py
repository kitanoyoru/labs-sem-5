from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict
from sqlalchemy import (
    BigInteger,
    Column,
    Date,
    Float,
    ForeignKey,
    Integer,
    String,
    Table,
    func,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class AdministratorModel(Base):
    __tablename__ = "administrator"

    ID = Column(Integer, primary_key=True, autoincrement=True)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String(15), nullable=False)

    employee = relationship("EmployeeModel", back_populates="administrator")

    system_metadata = relationship(
        "SystemMetadataModel", uselist=False, back_populates="administrator"
    )


class AdministratorOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    ID: int
    hashed_password: str
    full_name: str

    @staticmethod
    def from_model(administrator: AdministratorModel) -> AdministratorOut:
        return AdministratorOut.model_validate(administrator)


EmployeePositionTable = Table(
    "employee_position",
    Base.metadata,
    Column(
        "employee_id",
        Integer,
        ForeignKey("employee.ID", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True,
    ),
    Column(
        "position_id",
        Integer,
        ForeignKey("position.ID", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True,
    ),
)


class EmployeeModel(Base):
    __tablename__ = "employee"

    ID = Column(Integer, primary_key=True)

    full_name = Column(String)

    administrator_id = Column(Integer, ForeignKey("administrator.ID"))
    administrator = relationship("AdministratorModel", back_populates="employee")

    positions = relationship(
        "PositionModel", secondary=EmployeePositionTable, backref="employee"
    )

    payment_history = relationship("PaymentHistoryModel", back_populates="employee")


class CategoryModel(Base):
    __tablename__ = "category"

    ID = Column(Integer, primary_key=True, autoincrement=True)
    coefficient = Column(Float, nullable=False)
    change_date = Column(Date, nullable=False, default=func.current_date())

    position = relationship("PositionModel", back_populates="category")


class CategoryOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    coefficient: float
    change_date: datetime

    @staticmethod
    def from_model(category: CategoryModel) -> CategoryOut:
        return CategoryOut.model_validate(category)


class PositionModel(Base):
    __tablename__ = "position"

    ID = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(30), nullable=False)

    category_id = Column(
        Integer, ForeignKey("category.ID", ondelete="CASCADE", onupdate="CASCADE")
    )
    category = relationship("CategoryModel", back_populates="position")

    employees = relationship(
        "EmployeeModel", secondary=EmployeePositionTable, backref="position"
    )


class PositionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    ID: int

    name: str

    @staticmethod
    def from_model(position: PositionModel) -> PositionOut:
        return PositionOut.model_validate(position)


class PaymentHistoryModel(Base):
    __tablename__ = "payment_history"

    ID = Column(Integer, primary_key=True, autoincrement=True)

    month = Column(String(12), nullable=False)
    earnings = Column(BigInteger, nullable=False)
    payments = Column(BigInteger, nullable=False)
    deductions = Column(BigInteger, nullable=False)

    employee_id = Column(
        Integer, ForeignKey("employee.ID", ondelete="CASCADE", onupdate="CASCADE")
    )
    employee = relationship("EmployeeModel", back_populates="payment_history")


class PaymentHistoryOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    ID: int

    employee_id: int

    month: str
    earnings: int
    payments: int
    deductions: int

    @staticmethod
    def from_model(history: PaymentHistoryModel) -> PaymentHistoryOut:
        return PaymentHistoryOut.model_validate(history)


class SystemMetadataModel(Base):
    __tablename__ = "system_metadata"

    ID = Column(Integer, primary_key=True)

    trade_union_contribution = Column(BigInteger, nullable=False)
    income_tax = Column(BigInteger, nullable=False)
    minimum_salary = Column(BigInteger, nullable=False)
    pension_contribution = Column(BigInteger, nullable=False)

    administrator_id = Column(Integer, ForeignKey("administrator.ID"))
    administrator = relationship("AdministratorModel", back_populates="system_metadata")


class SystemMetadataOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    trade_union_contribution: int
    income_tax: int
    minimum_salary: int
    pension_contribution: int

    @staticmethod
    def from_model(system_metadata: SystemMetadataModel) -> SystemMetadataOut:
        return SystemMetadataOut.model_validate(system_metadata)


class EmployeeOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    ID: int
    full_name: str

    @staticmethod
    def from_model(employee: EmployeeModel) -> EmployeeOut:
        return EmployeeOut.model_validate(employee)
