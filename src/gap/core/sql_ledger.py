from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from typing import Optional
from gap.core.ledger import Ledger
from gap.core.manifest import GapManifest
from gap.core.state import GapStatus, StepData, StepStatus
from gap.core.models import Base, Project, Step, History

class SqlLedger(Ledger):
    def __init__(self, db_url: str, project_name: str, protocol: str, root: Path):
        self.root = root
        self.engine = create_engine(db_url)
        self.Session = sessionmaker(bind=self.engine)
        self.project_name = project_name
        self.protocol = protocol
        
        # Ensure tables exist (Auto-Migration)
        Base.metadata.create_all(self.engine)
        
        # Ensure project exists
        self._ensure_project()
        
    def _ensure_project(self):
        with self.Session() as session:
            project = session.query(Project).filter_by(name=self.project_name).first()
            if not project:
                # We need to ensure uniqueness if concurrent creation happens?
                # Simple check first.
                try:
                    project = Project(name=self.project_name, protocol=self.protocol)
                    session.add(project)
                    session.commit()
                except Exception:
                    session.rollback()
                    project = session.query(Project).filter_by(name=self.project_name).first()
                    
            self.project_id = project.id

    def get_status(self, manifest: GapManifest) -> GapStatus:
        with self.Session() as session:
            # Load stored steps from DB
            db_steps = session.query(Step).filter_by(project_id=self.project_id).all()
            db_map = {s.name: s for s in db_steps}
            
            # Re-calculate Real Status (Hybrid)
            real_status = GapStatus()
            
            for step in manifest.flow:
                # 1. Dependency Check (In Memory based on calculated real_status)
                dependencies_met = all(
                    real_status.steps.get(dep, StepData(status=StepStatus.LOCKED)).status == StepStatus.COMPLETE
                    for dep in step.needs
                )
                
                # 2. Check File Existence (The "Hybrid" Part)
                # Truth Source: DB vs FS
                
                db_step = db_map.get(step.step)
                
                # Check FS Reality
                artifact_path = self.root / step.artifact
                is_live = artifact_path.exists()
                
                proposal_path = self.root / ".gap/proposals" / step.artifact
                is_proposed = proposal_path.exists()
                
                current = StepStatus.LOCKED
                
                # Decision Logic
                if is_live:
                    # File exists -> Complete (regardless of DB, FS is ultimate truth)
                    # Ideally we sync this back to DB if DB thinks it's locked?
                    current = StepStatus.COMPLETE
                elif db_step and db_step.status == "complete":
                    # DB thinks complete, but file missing? 
                    # This is "Drift". We trust FS (Locked) or warn?
                    # For GAP, "Read-Open", if file is gone, it is NOT complete.
                    # So we fallback to Locked/Unlocked.
                    pass 
                elif is_proposed:
                    current = StepStatus.PENDING
                elif dependencies_met:
                    current = StepStatus.UNLOCKED
                    
                # DB Override/Enrichment
                # If DB is strictly ahead of FS (e.g. Approved but file not moved yet?), 
                # that shouldn't happen if 'approve' is atomic.
                
                # If Is Live, we mark Complete.
                # Use DB for metadata.
                
                step_data = StepData(status=current)
                if current == StepStatus.COMPLETE:
                     # Get metadata from DB if available
                     if db_step and db_step.status == "complete":
                         step_data.timestamp = db_step.timestamp.isoformat() if db_step.timestamp else None
                         step_data.approver = db_step.approver
                
                real_status.steps[step.step] = step_data
                
            return real_status

    def update_status(self, step: str, status: StepStatus, approver: str = "user", timestamp: Optional[datetime] = None) -> None:
        with self.Session() as session:
            # Find Step
            db_step = session.query(Step).filter_by(project_id=self.project_id, name=step).first()
            
            if not db_step:
                # Create if new
                db_step = Step(
                    project_id=self.project_id, 
                    name=step, 
                    status=status.value
                )
                session.add(db_step)
            else:
                # Track History
                history = History(
                    step_id=db_step.id,
                    old_status=db_step.status,
                    new_status=status.value,
                    actor=approver,
                    timestamp=timestamp or datetime.utcnow()
                )
                session.add(history)
                
                # Update
                db_step.status = status.value
            
            if status == StepStatus.COMPLETE:
                db_step.approver = approver
                db_step.timestamp = timestamp or datetime.utcnow()
                
            session.commit()
