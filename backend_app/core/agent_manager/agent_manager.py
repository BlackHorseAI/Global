from sqlalchemy.orm import Session
from ..database import models
from ..schemas import AgentCreate

def get_agent(db: Session, agent_id: int):
    return db.query(models.Agent).filter(models.Agent.id == agent_id).first()

def get_agents_by_owner(db: Session, owner_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Agent).filter(models.Agent.owner_id == owner_id).offset(skip).limit(limit).all()

def create_agent(db: Session, agent: AgentCreate, owner_id: int):
    db_agent = models.Agent(**agent.model_dump(), owner_id=owner_id)
    db.add(db_agent)
    db.commit()
    db.refresh(db_agent)
    return db_agent