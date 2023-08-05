from helix_events_sdk.schemas.audit_enums import AuditAction, AuditActionType, ResourceType


class Audit:
    def __init__(
        self, patient_id: str, user_id: str, user_role: str, ip_address: str,
        client_slug: str,
        action: AuditAction, action_type: AuditActionType,
        accessed_resource: ResourceType
    ):
        self.patient_id = patient_id
        self.user_id = user_id
        self.action = action.value
        self.user_role = user_role
        self.ip_address = ip_address
        self.client_slug = client_slug
        self.action_type = action_type.value
        self.source_system = "b.well"
        self.document_type = accessed_resource.value
