# OpsFlow: staff and device readiness

## Who needs this

A fictional six-site Canadian care network with a central IT team, local coordinators, rotating staff, and predictable placement start/end dates. Each subscribing care organization is a separate tenant. Each site belongs to one tenant. The paying buyer is the IT operations lead; daily users are IT operators and site coordinators.

The product addresses the gap between a support ticket being updated and equipment actually being ready. It is a focused operations system, not a replacement for ServiceNow, HR software, clinical records, procurement ERP, or device-management software.

## Personal motivation and boundaries

The design connects IT support and workflow-automation interests with the experience of starting internships and moving between teams. It is an independent project using fabricated scenarios. No employer workflows, proprietary data, staff records, or patient information are reproduced. Device wipe evidence is recorded from an authorized operator or future MDM adapter; this API does not itself erase hardware. Compliance evidence is not a legal certification.

## A complete first release

1. A site coordinator requests a kit for a fictional staff member: location, role template, start/end dates, and requested equipment.
2. IT checks compatible stock and reserves a device atomically. If stock is unavailable, a purchase request enters an approval queue.
3. An independent approver accepts or rejects the requested spend, recording a reason and the request version.
4. A vendor shipment is created through a manual adapter first. Tracking events update expected delivery and readiness risk.
5. The receiving site acknowledges delivery. IT records setup/checklist completion and staff custody. A request is ready only when required checks pass.
6. At end date, a return workflow tracks collection, inspection, and wipe evidence. A device cannot return to available inventory until those gates pass.

## Deliberate scope limits

Start with laptops and a small set of accessory kit items. Use manual shipment events and mock email transport first. No real carrier contract, purchasing/payment execution, payroll, patient data, live device control, autonomous AI, or nationwide logistics optimizer in the MVP. A later ServiceNow adapter can exchange request IDs and state after the core workflow is reliable.

## Data and state

Organization, Site, User, Membership, StaffPlacement, KitTemplate, ReadinessRequest, ChecklistItem, Asset, Reservation, Assignment, Vendor, PurchaseRequest, Approval, Shipment, ShipmentEvent, ReturnCase, EvidenceRecord, AuditEvent.

ReadinessRequest: draft -> submitted -> approved -> preparing -> dispatched -> ready; rejected/cancelled are explicit terminal alternatives. Stock-backed requests can bypass purchase approval according to a documented policy, but cannot bypass authorization or readiness checks. ReturnCase: opened -> in_transit -> received -> inspected -> wipe_verified -> closed. An exception requires an authorized reason and an audit event.

## Rules worth demonstrating

- Reservation is tenant-scoped and expires; two concurrent requests cannot reserve one laptop.
- A late delivery does not mark a request ready. Readiness is derived from required checklist state, not a manually optimistic label.
- A user may belong to multiple organizations with different roles; changing the selected tenant does not grant access.
- A requester cannot approve their own purchase. Changed amounts invalidate earlier approval.
- Duplicate carrier events and reminder retries have no duplicate side effects.
- A device with missing return or wipe evidence cannot be reissued.
- Evidence includes a reference, actor, timestamp, and reason; no patient or diagnostic information.

## Useful measures (targets, not measured results)

Percentage ready by start date; overdue returns; median request-to-ready time; proportion fulfilled from reusable inventory; approval turnaround; duplicate reservation failures; worker retry/failure counts. Define event timestamps and a denominator before claiming improvement.

## Demo fixture

Create Cedar Care and Harbour Care as independent fictional tenants. Cedar has Hamilton and Toronto sites, two laptops, three placements, one delayed shipment, and one overdue return. Show the complete happy path, a stock shortage, a rejected self-approval, a duplicate reservation race, and denied access to Harbour records.
