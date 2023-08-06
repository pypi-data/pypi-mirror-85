# helix.events.sdk

The helix.events.sdk package facilitates sending strongly typed events within the helix architecure. Currently one type of event, AuditEvent, is supported. The following code snippet shows how to instantiate and send and audit event:

```python
# create the AuditEvent
event = AuditEvent(Source.BWELLBACKEND, Audit(patient_id="1",
                                              user_id="1",
                                              user_role="Patient",
                                              ip_address="192.168.1.1",
                                              action=AuditAction.READ,
                                              action_type=AuditActionType.VIEW,
                                              accessed_resource=ResourceType.DIAGNOSES))

# create an event writer
event_writer = EventWriter(get_logger())

# write the event
event_writer.write_event(event=event)
```

Currently EventWriter simply logs the event, but in future versions will publish the event to the appropriate event store.
