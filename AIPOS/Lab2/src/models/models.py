from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict
from sqlalchemy import (
    BigInteger,
    Column,
    Date,
    Float,
    ForeignKey,
    Integer,
    String,
    func,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class AdministratorModel(Base):
    __tablename__ = "t_administrator"

    ID = Column(Integer, primary_key=True, autoincrement=True)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String(15), nullable=False)

    employee = relationship("EmployeeModel", back_populates="t_administrator")

    system_metadata = relationship(
        "SystemMetadataModel", uselist=False, back_populates="t_administrator"
    )


class AdministratorOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    ID: int
    hashed_password: str
    full_name: str

    @staticmethod
    def from_model(administrator: AdministratorModel) -> AdministratorOut:
        return AdministratorOut.model_validate(administrator)


class Employee_Position(Base):
    __tablename__ = "t_employee_position"

    employee_id = Column(
        Integer,
        ForeignKey("t_employee.ID", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True,
    )
    position_id = Column(
        Integer,
        ForeignKey("t_position.ID", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True,
    )


class EmployeeModel(Base):
    __tablename__ = "t_employee"

    ID = Column(Integer, primary_key=True)

    full_name = Column(String, index=True)

    administrator_id = Column(Integer, ForeignKey("t_administrator.ID"))
    administrator = relationship("AdministratorModel", back_populates="t_employee")

    positions = relationship(
        "PositionModel", secondary=Employee_Position, backref="t_employee"
    )

    payment_history = relationship("PaymentHistoryModel", back_populates="t_employee")


class EmployeeOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    ID: int
    full_name: str

    @staticmethod
    def from_model(employee: EmployeeModel) -> EmployeeModel:
        return EmployeeOut.model_validate(employee)


class CategoryModel(Base):
    __tablename__ = "t_category"

    ID = Column(Integer, primary_key=True, autoincrement=True)
    coefficient = Column(Float, nullable=False)
    change_date = Column(Date, nullable=False, default=func.current_date())

    position = relationship("PositionModel", back_populates="t_category")


class CategoryOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    coefficient: float
    change_date: datetime

    @staticmethod
    def from_model(category: CategoryModel) -> CategoryOut:
        return CategoryOut.model_validate(category)


class PositionModel(Base):
    __tablename__ = "t_position"

    ID = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(30), nullable=False)

    category_id = Column(
        Integer, ForeignKey("t_category.ID", ondelete="CASCADE", onupdate="CASCADE")
    )
    category = relationship("CategoryModel", back_populates="t_position")


class PaymentHistoryModel(Base):
    __tablename__ = "t_payment_history"

    ID = Column(Integer, primary_key=True, autoincrement=True)

    month = Column(String(12), nullable=False, index=True)
    earnings = Column(BigInteger, nullable=False)
    payments = Column(BigInteger, nullable=False)
    deductions = Column(BigInteger, nullable=False)

    employee_id = Column(
        Integer, ForeignKey("t_employee.ID", ondelete="CASCADE", onupdate="CASCADE")
    )
    employee = relationship("EmployeeModel", back_populates="t_payment_history")


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
    __tablename__ = "t_system_metadata"

    ID = Column(Integer, primary_key=True)

    trade_union_contribution = Column(BigInteger, nullable=False)
    income_tax = Column(BigInteger, nullable=False)
    minimum_salary = Column(BigInteger, nullable=False)
    pension_contribution = Column(BigInteger, nullable=False)

    administrator_id = Column(Integer, ForeignKey("t_administrator.ID"))
    administrator = relationship(
        "AdministratorModel", back_populates="t_system_metadata"
    )


class SystemMetadataOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    trade_union_contribution: int
    income_tax: int
    minimum_salary: int
    pension_contribution: int

    @staticmethod
    def from_model(system_metadata: SystemMetadataModel) -> SystemMetadataOut:
        return SystemMetadataOut.model_validate(system_metadata)
