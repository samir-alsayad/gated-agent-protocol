class FlowStep:
    def __init__(self, name, artifact, category):
        # We shadow the manifest FlowStep name/step/artifact concept
        self.name = name
        self.step = name
        self.artifact = artifact
        self.category = category

class Task:
    """Represents an execution task parsed from tasks.md"""
    def __init__(self, id, file, status="pending"):
        self.id = id
        self.file = file
        self.status = status

    def __repr__(self):
        return f"Task({self.id}, {self.file}, {self.status})"
