from enum import Enum


class AuditAction(Enum):
    READ = "Read"
    WRITE = "Write"
    UPDATE = "Update"


class AuditActionType(Enum):
    VIEW = "View"
    EXPORT = "Export"
    MODIFY = "Modify"


class ResourceType(Enum):
    NOTE = "Note"
    DEMOGRAPHICS = "Demographics"
    VITALS = "Vitals"
    CLAIMS = "Claims"
    OBSERVATIONS = "Observations"
    DIAGNOSES = "Diagnoses"
    PROCEDURES = "Procedures"
