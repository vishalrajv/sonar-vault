from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from models.base import Base

platform_project_association = Table(
    "platform_projects",
    Base.metadata,
    Column("platform_id", Integer, ForeignKey("platforms.id"), primary_key=True),
    Column("project_id", Integer, ForeignKey("projects.id"), primary_key=True),
)


class Platform(Base):
    __tablename__ = "platforms"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True, index=True)

    projects = relationship(
        "Project", secondary=platform_project_association, back_populates="platforms"
    )
    subsystems = relationship("Subsystem", back_populates="platform")

    def __repr__(self):
        return f"<Platform(name='{self.name}')>"


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True, index=True)

    platforms = relationship(
        "Platform", secondary=platform_project_association, back_populates="projects"
    )
    subsystems = relationship("Subsystem", back_populates="project")

    def __repr__(self):
        return f"<Project(name='{self.name}')>"


class Subsystem(Base):
    __tablename__ = "subsystems"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    platform_id = Column(Integer, ForeignKey("platforms.id"), nullable=True)

    project = relationship("Project", back_populates="subsystems")
    platform = relationship("Platform", back_populates="subsystems")

    def __repr__(self):
        return f"<Subsystem(name='{self.name}', project_id={self.project_id})>"
