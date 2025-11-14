
# Install fhir.resources if not already installed
!pip install fhir.resources

from fhir.resources.patient import Patient
from fhir.resources.observation import Observation
from fhir.resources.medicationrequest import MedicationRequest
from fhir.resources.practitioner import Practitioner
from fhir.resources.coding import Coding
from fhir.resources.codeableconcept import CodeableConcept
from fhir.resources.codeablereference import CodeableReference

# -----------------------
# Create FHIR-compliant medication structure (FHIR R5)
# -----------------------

# Coding for the medication
medication_coding = Coding(
    system="http://www.nlm.nih.gov/research/umls/rxnorm",
    code="197361",
    display="Lisinopril 10 MG Oral Tablet"
)

# CodeableConcept wraps the coding
medication_concept = CodeableConcept(
    coding=[medication_coding]
)

# Wrap CodeableConcept inside CodeableReference (R5 requirement)
medication_reference = CodeableReference(
    concept=medication_concept
)

# -----------------------
# Patient resource
# -----------------------
patient_json = {
    "resourceType": "Patient",
    "id": "patient-hypertension-001",
    "name": [{"family": "Okeke", "given": ["Chinedu"]}],
    "gender": "male",
    "birthDate": "1970-04-12"
}

# -----------------------
# Observation resource
# -----------------------
observation_json = {
    "resourceType": "Observation",
    "id": "bp-observation-001",
    "status": "final",
    "category": [{
        "coding": [{
            "system": "http://terminology.hl7.org/CodeSystem/observation-category",
            "code": "vital-signs",
            "display": "Vital Signs"
        }]
    }],
    "code": {
        "coding": [{
            "system": "http://loinc.org",
            "code": "8480-6",
            "display": "Systolic Blood Pressure"
        }]
    },
    "subject": {"reference": "Patient/patient-hypertension-001"},
    "effectiveDateTime": "2025-07-04T10:30:00+02:00",
    "valueQuantity": {
        "value": 145,
        "unit": "mmHg",
        "system": "http://unitsofmeasure.org",
        "code": "mm[Hg]"
    }
}

# -----------------------
# Practitioner resource
# -----------------------
practitioner_json = {
    "resourceType": "Practitioner",
    "id": "practitioner-001",
    "name": [{"family": "Müller", "given": ["Anja"]}],
    "qualification": [{"code": {"text": "General Practitioner"}}]
}

# -----------------------
# Create MedicationRequest
# -----------------------
med_request = MedicationRequest(
    resourceType="MedicationRequest",
    id="medreq-001",
    status="active",
    intent="order",
    medication=medication_reference,  # ✅ Correct type: CodeableReference
    subject={"reference": "Patient/patient-hypertension-001"},
    authoredOn="2025-07-01",
    requester={"reference": "Practitioner/practitioner-001"}
)

# -----------------------
# Validation & Output
# -----------------------
try:
    patient = Patient(**patient_json)
    observation = Observation(**observation_json)
    practitioner = Practitioner(**practitioner_json)

    print("✅ All FHIR resources loaded and validated successfully:")
    print("Patient ID:", patient.id)
    print("BP Observation:", observation.code.coding[0].display)
    print("Medication Code:", med_request.medication.concept.coding[0].code)
    print("Practitioner Name:", practitioner.name[0].given[0], practitioner.name[0].family)

    # Save JSON outputs
    with open("patient.json", "w") as f:
        f.write(patient.json(indent=2))
    with open("observation.json", "w") as f:
        f.write(observation.json(indent=2))
    with open("medication_request.json", "w") as f:
        f.write(med_request.json(indent=2))
    with open("practitioner.json", "w") as f:
        f.write(practitioner.json(indent=2))

except Exception as e:
    print("❌ Validation failed:", str(e))
