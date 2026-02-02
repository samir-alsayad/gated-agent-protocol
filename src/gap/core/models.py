from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()

class Project(Base):
    __tablename__ = 'projects'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    protocol = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    steps = relationship("Step", back_populates="project")

class Step(Base):
    __tablename__ = 'steps'
    
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('projects.id'), nullable=False)
    name = Column(String, nullable=False) # e.g. 'requirements'
    status = Column(String, nullable=False) # 'locked', 'unlocked', 'complete'
    
    # Metadata for 'complete' steps
    approver = Column(String)
    timestamp = Column(DateTime)
    
    project = relationship("Project", back_populates="steps")
    
    # One entry per step per project
    __table_args__ = (UniqueConstraint('project_id', 'name', name='uix_project_step'),)

class History(Base):
    __tablename__ = 'history'
    
    id = Column(Integer, primary_key=True)
    step_id = Column(Integer, ForeignKey('steps.id'))
    old_status = Column(String)
    new_status = Column(String)
    actor = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
