from __future__ import annotations

from sqlalchemy import Column, ForeignKey, Integer, String, BigInteger, Float, Date, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()

class AdministratorModel(Base):
    __tablename__ = 'administrator'

    ID = Column(Integer, primary_key=True)
    full_name = Column(String(15), nullable=False)

    system_metadata_id = Column(Integer, ForeignKey('system_metadata.ID', ondelete='CASCADE', onupdate='CASCADE'))
    system_metadata = relationship("SystemMetadataModel")

class Employee(Base):
    __tablename__ = "employee"

    ID = Column(Integer, primary_key=True)
    fullname = Column(String)

    administrator_id = Column(Integer, ForeignKey("administrator.ID"))
    administrator = relationship("AdministratorModel", back_populates="employee")

    payment_history = relationship("PaymentHistoryModel", back_populates="employee")

class CategoryModel(Base):
    __tablename__ = 'category'

    ID = Column(Integer, primary_key=True)
    coefficient = Column(Float, nullable=False)
    change_date = Column(Date, nullable=False, default=func.current_date())


class PositionModel(Base):
    __tablename__ = 'position'

    ID = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False)

    category_id = Column(Integer, ForeignKey('category.ID', ondelete='CASCADE', onupdate='CASCADE'))
    category = relationship("CategoryModel", back_populates="position")

class Employee_Position(Base):
    __tablename__ = 'employee_position'

    employee_id = Column(Integer, ForeignKey('employee.ID', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)
    position_id = Column(Integer, ForeignKey('position.ID', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)


class PaymentHistoryModel(Base):
    __tablename__ = "payment_history"

    ID = Column(Integer, primary_key=True)

    month = Column(String(12), nullable=False)
    earnings = Column(BigInteger, nullable=False)
    payments = Column(BigInteger, nullable=False)
    deductions = Column(BigInteger, nullable=False)

    employee_od = Column(Integer, ForeignKey("employee.ID", ondelete="CASCADE", onupdate="CASCADE"))
    employee = relationship("EmployeeModel", back_populates="payment_history")


class SystemMetadataModel(Base):
    __tablename__ = 'system_metadata'

    ID = Column(Integer, primary_key=True)
    trade_union_contribution = Column(BigInteger, nullable=False)
    income_tax = Column(BigInteger, nullable=False)
    minimum_salary = Column(BigInteger, nullable=False)
    pension_contribution = Column(BigInteger, nullable=False)
