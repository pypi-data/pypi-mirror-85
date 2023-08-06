import uuid
from datetime import datetime

from cloudevents.http import CloudEvent
from fhir.resources.codeableconcept import CodeableConcept
from fhir.resources.coding import Coding
from fhir.resources.fhirdate import FHIRDate
from fhir.resources.fhirreference import FHIRReference

from fhir.resources.auditevent import AuditEvent as FhirAuditEvent, AuditEventSource, AuditEventAgent, \
    AuditEventAgentNetwork, AuditEventEntity

from helix_events_sdk.schemas.audit import Audit
from helix_events_sdk.schemas.source import Source


class AuditEvent(CloudEvent):  # type: ignore
    def __init__(self, source: Source, data: Audit):
        event_id = str(uuid.uuid4())
        self.id = event_id
        attributes = {
            "type": "com.bwell.audit",
            "source": source.value,
            "id": event_id
        }
        fhir_audit_event = self._get_fhir_audit_event(data)

        super().__init__(
            attributes=attributes, data=fhir_audit_event.as_json()
        )

    def _get_fhir_audit_event(self, data: Audit) -> FhirAuditEvent:
        fhir_audit_event = FhirAuditEvent()
        fhir_audit_event.id = self.id
        fhir_audit_event.type = self._get_event_type(data)
        fhir_audit_event.action = data.action
        fhir_audit_event.recorded = self._get_event_recorded()
        user_agent = self._get_user_agent(data)
        patient_agent = self._get_patient_agent(data)
        organization_agent = self._get_organization_agent(data)
        fhir_audit_event.agent = [user_agent, patient_agent, organization_agent]
        fhir_audit_event.source = self._get_audit_event_source(data)
        fhir_audit_event.entity = [self._get_audit_event_entity(data)]
        return fhir_audit_event

    def _get_audit_event_entity(self, data: Audit) -> AuditEventEntity:
        entity = AuditEventEntity()
        entity.name = data.document_type
        return entity

    def _get_audit_event_source(self, data: Audit) -> AuditEventSource:
        audit_event_source = AuditEventSource()
        audit_event_source.observer = FHIRReference()
        audit_event_source.site = data.source_system
        return audit_event_source

    def _get_patient_agent(self, data: Audit) -> AuditEventAgent:
        patient_agent = AuditEventAgent()
        patient_agent.requestor = False
        patient_agent.altId = data.patient_id
        return patient_agent

    def _get_user_agent(self, data: Audit) -> AuditEventAgent:
        user_agent = AuditEventAgent()
        user_agent.requestor = True
        user_agent.altId = data.user_id
        user_agent.network = AuditEventAgentNetwork(
            jsondict={"address": data.ip_address}
        )
        user_agent.role = [
            CodeableConcept(
                jsondict={
                    "coding": [{
                        "code": data.user_role
                    }],
                    "text": data.user_role
                }
            )
        ]
        return user_agent

    def _get_organization_agent(self, data: Audit) -> AuditEventAgent:
        organization_agent = AuditEventAgent()
        organization_agent.requestor = False
        organization_agent.altId = data.client_slug
        organization_agent.who = FHIRReference(jsondict={
            "reference": f"Organization/{data.client_slug}"
        })
        return organization_agent

    def _get_event_type(self, data: Audit) -> Coding:
        event_type = Coding()
        event_type.code = data.action_type
        event_type.display = data.action_type
        return event_type

    def _get_event_recorded(self) -> FHIRDate:
        recorded = FHIRDate()
        recorded.date = datetime.utcnow()
        return recorded
