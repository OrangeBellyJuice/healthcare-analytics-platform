import pytest
from pydantic import ValidationError

from src.validations.models import (
    Condition,
    Encounter,
    MedicationRequest,
    Observation,
    ObservationComponent,
    Organization,
    Patient,
    Practitioner,
    Procedure,
)

valid_encounter = {
    "resourceType": "Encounter",
    "id": "c2aadfa1-256b-c450-48e9-0a5e44171a14",
    "status": "finished",
    "class": {
        "system": "http://terminology.hl7.org/CodeSystem/v3-ActCode",
        "code": "AMB",
    },
    "type": [
        {
            "coding": [
                {
                    "system": "http://snomed.info/sct",
                    "code": "185345009",
                    "display": "Encounter for symptom (procedure)",
                }
            ],
            "text": "Encounter for symptom (procedure)",
        }
    ],
    "subject": {
        "reference": "urn:uuid:c2aadfa1-256b-c450-bcd5-442316fa4fe9",
        "display": "Mr. Aaron697 DuBuque211",
    },
    "participant": [
        {
            "individual": {
                "reference": (
                    "Practitioner?identifier=http://hl7.org/fhir/sid/us-npi|9999976399"
                ),
                "display": "Dr. Arlene209 Olson653",
            }
        }
    ],
    "period": {
        "start": "1997-11-16T08:55:27-08:00",
        "end": "1997-11-16T09:10:27-08:00",
    },
    "reasonCode": [
        {
            "coding": [
                {
                    "system": "http://snomed.info/sct",
                    "code": "444814009",
                    "display": "Viral sinusitis (disorder)",
                }
            ]
        }
    ],
    "serviceProvider": {
        "reference": (
            "Organization?identifier="
            "https://github.com/synthetichealth/synthea|"
            "0e58807a-a5f2-3e7d-a9d6-eca59bc3df95"
        ),
        "display": "Shoreline Medical",
    },
}


valid_condition = {
    "resourceType": "Condition",
    "id": "c2aadfa1-256b-c450-e2a4-42a0880217f0",
    "clinicalStatus": {
        "coding": [
            {
                "system": ("http://terminology.hl7.org/CodeSystem/condition-clinical"),
                "code": "resolved",
            }
        ]
    },
    "verificationStatus": {
        "coding": [
            {
                "system": (
                    "http://terminology.hl7.org/CodeSystem/condition-ver-status"
                ),
                "code": "confirmed",
            }
        ]
    },
    "code": {
        "coding": [
            {
                "system": "http://snomed.info/sct",
                "code": "109838007",
                "display": ("Overlapping malignant neoplasm of colon (disorder)"),
            }
        ],
        "text": "Overlapping malignant neoplasm of colon (disorder)",
    },
    "subject": {
        "reference": "urn:uuid:c2aadfa1-256b-c450-bcd5-442316fa4fe9",
    },
    "encounter": {
        "reference": "urn:uuid:c2aadfa1-256b-c450-8612-54e6414afc28",
    },
    "onsetDateTime": "2002-06-18T00:15:36-07:00",
    "abatementDateTime": "2004-10-23T21:02:28-07:00",
    "recordedDate": "2002-06-18T00:15:36-07:00",
}

valid_patient = {
    "resourceType": "Patient",
    "id": "c2aadfa1-256b-c450-bcd5-442316fa4fe9",
    "name": [
        {
            "use": "official",
            "family": "DuBuque211",
            "given": ["Aaron697"],
            "prefix": ["Mr."],
        }
    ],
    "gender": "male",
    "birthDate": "1951-04-21",
    "deceasedDateTime": "2007-05-20T04:55:27-07:00",
    "address": [
        {
            "line": ["818 Rodriguez Junction Unit 57"],
            "city": "Sidney",
            "state": "BC",
            "postalCode": "V8L",
            "country": "CA",
        }
    ],
    "maritalStatus": {
        "text": "Married",
    },
    "multipleBirthBoolean": False,
}

valid_practitioner = {
    "resourceType": "Practitioner",
    "id": "4ac6772e-f4cd-3862-b53c-bb433031afc9",
    "name": [
        {
            "family": "Schumm995",
            "given": ["Hilari0934"],
            "prefix": ["Dr."],
        }
    ],
    "address": [
        {
            "line": ["201-7315 edmonds street"],
            "city": "Burnaby",
            "state": "BC",
            "postalCode": "V3N 1A7",
            "country": "CA",
        }
    ],
    "gender": "male",
}

valid_organization = {
    "resourceType": "Organization",
    "id": "231f25bb-2bdc-31e6-b187-3e666cb9f8fa",
    "name": "Primecare Medical Centre",
    "address": [
        {
            "line": ["201-7315 edmonds street"],
            "city": "Burnaby",
            "state": "BC",
            "postalCode": "V3N 1A7",
            "country": "CA",
        }
    ],
}

valid_observation = {
    "resourceType": "Observation",
    "id": "94697183-8162-51cb-d85c-1177d6dd5301",
    "status": "final",
    "category": [
        {
            "coding": [
                {
                    "system": "http://terminology.hl7.org/CodeSystem/observation-category",
                    "code": "vital-signs",
                    "display": "Vital signs",
                }
            ]
        }
    ],
    "code": {
        "coding": [
            {
                "system": "http://loinc.org",
                "code": "8302-2",
                "display": "Body Height",
            }
        ],
        "text": "Body Height",
    },
    "subject": {"reference": "urn:uuid:94697183-8162-51cb-016a-7aaefbb845ba"},
    "encounter": {"reference": "urn:uuid:94697183-8162-51cb-d5a1-40d07064b4e1"},
    "effectiveDateTime": "2016-10-12T16:44:44-07:00",
    "issued": "2016-10-12T16:44:44.253-07:00",
    "valueQuantity": {
        "value": 56.6,
        "unit": "cm",
        "system": "http://unitsofmeasure.org",
        "code": "cm",
    },
}

valid_coded_observation = {
    "resourceType": "Observation",
    "id": "94697183-8162-51cb-2b7c-2d93157ba875",
    "status": "final",
    "category": [
        {
            "coding": [
                {
                    "system": "http://terminology.hl7.org/CodeSystem/observation-category",
                    "code": "social-history",
                    "display": "Social history",
                }
            ]
        }
    ],
    "code": {
        "coding": [
            {
                "system": "http://loinc.org",
                "code": "72166-2",
                "display": "Tobacco smoking status",
            }
        ],
        "text": "Tobacco smoking status",
    },
    "subject": {"reference": "urn:uuid:94697183-8162-51cb-016a-7aaefbb845ba"},
    "encounter": {"reference": "urn:uuid:94697183-8162-51cb-d5a1-40d07064b4e1"},
    "effectiveDateTime": "2016-10-12T16:44:44-07:00",
    "issued": "2016-10-12T16:44:44.253-07:00",
    "valueCodeableConcept": {
        "coding": [
            {
                "system": "http://snomed.info/sct",
                "code": "266919005",
                "display": "Never smoked tobacco (finding)",
            }
        ],
        "text": "Never smoked tobacco (finding)",
    },
}

valid_procedure = {
    "resourceType": "Procedure",
    "id": "94697183-8162-51cb-f2eb-3fab08e350f7",
    "status": "completed",
    "code": {
        "coding": [
            {
                "system": "http://snomed.info/sct",
                "code": "23426006",
                "display": "Measurement of respiratory function (procedure)",
            }
        ],
        "text": "Measurement of respiratory function (procedure)",
    },
    "subject": {"reference": "urn:uuid:94697183-8162-51cb-016a-7aaefbb845ba"},
    "encounter": {"reference": "urn:uuid:94697183-8162-51cb-10f8-1df2d9f6e882"},
    "performedPeriod": {
        "start": "2024-04-01T10:44:44-07:00",
        "end": "2024-04-01T11:03:43-07:00",
    },
    "reasonReference": [
        {
            "reference": "urn:uuid:94697183-8162-51cb-b39b-2b8c6b950f1b",
            "display": "Acute bronchitis (disorder)",
        }
    ],
}

valid_component_observation = {
    "resourceType": "Observation",
    "id": "94697183-8162-51cb-1249-ce8a923a40f1",
    "status": "final",
    "category": [
        {
            "coding": [
                {
                    "system": "http://terminology.hl7.org/CodeSystem/observation-category",
                    "code": "vital-signs",
                    "display": "Vital signs",
                }
            ]
        }
    ],
    "code": {
        "coding": [
            {
                "system": "http://loinc.org",
                "code": "85354-9",
                "display": "Blood pressure panel with all children optional",
            }
        ],
        "text": "Blood pressure panel with all children optional",
    },
    "subject": {"reference": "urn:uuid:94697183-8162-51cb-016a-7aaefbb845ba"},
    "encounter": {"reference": "urn:uuid:94697183-8162-51cb-d5a1-40d07064b4e1"},
    "effectiveDateTime": "2016-10-12T16:44:44-07:00",
    "issued": "2016-10-12T16:44:44.253-07:00",
    "component": [
        {
            "code": {
                "coding": [
                    {
                        "system": "http://loinc.org",
                        "code": "8462-4",
                        "display": "Diastolic Blood Pressure",
                    }
                ]
            },
            "valueQuantity": {
                "value": 68,
                "unit": "mm[Hg]",
                "system": "http://unitsofmeasure.org",
                "code": "mm[Hg]",
            },
        },
        {
            "code": {
                "coding": [
                    {
                        "system": "http://loinc.org",
                        "code": "8480-6",
                        "display": "Systolic Blood Pressure",
                    }
                ]
            },
            "valueQuantity": {
                "value": 111,
                "unit": "mm[Hg]",
                "system": "http://unitsofmeasure.org",
                "code": "mm[Hg]",
            },
        },
    ],
}

valid_medication_request = {
    "resourceType": "MedicationRequest",
    "id": "94697183-8162-51cb-8ffd-e654fe53c12c",
    "status": "completed",
    "intent": "order",
    "medicationCodeableConcept": {
        "coding": [
            {
                "system": "http://www.nlm.nih.gov/research/umls/rxnorm",
                "code": "308192",
                "display": "Amoxicillin 500 MG Oral Tablet",
            }
        ],
        "text": "Amoxicillin 500 MG Oral Tablet",
    },
    "subject": {"reference": "urn:uuid:94697183-8162-51cb-016a-7aaefbb845ba"},
    "encounter": {"reference": "urn:uuid:94697183-8162-51cb-fd4f-db0eeae721a6"},
    "authoredOn": "2017-09-02T16:44:44-07:00",
    "requester": {
        "reference": (
            "Practitioner?identifier=http://hl7.org/fhir/sid/us-npi|9999997791"
        ),
        "display": "Dr. Marcy588 Hamill307",
    },
    "dosageInstruction": [
        {
            "sequence": 1,
            "text": (
                "Take at regular intervals. Complete the prescribed "
                "course unless otherwise directed (qualifier value)"
            ),
            "timing": {
                "repeat": {
                    "frequency": 3,
                    "period": 1.0,
                    "periodUnit": "d",
                }
            },
            "asNeededBoolean": False,
            "doseAndRate": [
                {
                    "doseQuantity": {
                        "value": 1.0,
                    }
                }
            ],
        }
    ],
}


def test_valid_observation_passes_validation():
    result = Observation.model_validate(valid_observation)

    assert result.id == "94697183-8162-51cb-d85c-1177d6dd5301"
    assert result.resourceType == "Observation"
    assert result.status == "final"
    assert result.code.coding[0].code == "8302-2"
    assert result.valueQuantity is not None
    assert result.valueQuantity.value == 56.6


def test_coded_observation_passes_validation():
    result = Observation.model_validate(valid_coded_observation)

    assert result.valueCodeableConcept is not None
    assert result.valueCodeableConcept.coding[0].code == "266919005"
    assert result.valueCodeableConcept.text == ("Never smoked tobacco (finding)")


def test_component_observation_passes_validation():
    result = Observation.model_validate(valid_component_observation)

    assert result.component is not None
    assert len(result.component) == 2

    assert result.component[0].code.coding[0].code == "8462-4"
    assert result.component[0].valueQuantity is not None
    assert result.component[0].valueQuantity.value == 68

    assert result.component[1].code.coding[0].code == "8480-6"
    assert result.component[1].valueQuantity is not None
    assert result.component[1].valueQuantity.value == 111


def test_observation_component_with_string_value_passes_validation():
    component = {
        "code": {
            "coding": [
                {
                    "system": "http://loinc.org",
                    "code": "56799-0",
                    "display": "Address",
                }
            ]
        },
        "valueString": "851 Barton Ferry",
    }

    result = ObservationComponent.model_validate(component)

    assert result.valueString == "851 Barton Ferry"


def test_observation_component_with_coded_value_passes_validation():
    component = {
        "code": {
            "coding": [
                {
                    "system": "http://loinc.org",
                    "code": "67875-5",
                    "display": "Employment status - current",
                }
            ]
        },
        "valueCodeableConcept": {
            "coding": [
                {
                    "system": "http://loinc.org",
                    "code": "LA17956-6",
                    "display": "Unemployed",
                }
            ],
            "text": "Unemployed",
        },
    }

    result = ObservationComponent.model_validate(component)

    assert result.valueCodeableConcept is not None
    assert result.valueCodeableConcept.coding[0].code == "LA17956-6"


def test_valid_procedure_passes_validation():
    result = Procedure.model_validate(valid_procedure)

    assert result.id == "94697183-8162-51cb-f2eb-3fab08e350f7"
    assert result.resourceType == "Procedure"
    assert result.status == "completed"
    assert result.code.coding[0].code == "23426006"
    assert result.reasonReference[0].display == ("Acute bronchitis (disorder)")


def test_valid_medication_request_passes_validation():
    result = MedicationRequest.model_validate(valid_medication_request)

    assert result.id == "94697183-8162-51cb-8ffd-e654fe53c12c"
    assert result.resourceType == "MedicationRequest"
    assert result.status == "completed"
    assert result.medicationCodeableConcept.coding[0].code == "308192"
    assert result.dosageInstruction[0].timing.repeat.frequency == 3


def test_observation_missing_code_fails_validation():
    invalid_observation = valid_observation.copy()
    invalid_observation.pop("code")

    with pytest.raises(ValidationError):
        Observation.model_validate(invalid_observation)


def test_procedure_missing_code_fails_validation():
    invalid_procedure = valid_procedure.copy()
    invalid_procedure.pop("code")

    with pytest.raises(ValidationError):
        Procedure.model_validate(invalid_procedure)


def test_medication_request_missing_medication_fails_validation():
    invalid_medication_request = valid_medication_request.copy()
    invalid_medication_request.pop("medicationCodeableConcept")

    with pytest.raises(ValidationError):
        MedicationRequest.model_validate(invalid_medication_request)


def test_medication_request_without_dosage_instruction_passes_validation():
    medication_request = valid_medication_request.copy()
    medication_request.pop("dosageInstruction")

    result = MedicationRequest.model_validate(medication_request)

    assert result.dosageInstruction is None


def test_procedure_without_reason_passes_validation():
    procedure = valid_procedure.copy()
    procedure.pop("reasonReference")

    result = Procedure.model_validate(procedure)

    assert result.reasonReference is None


def test_valid_encounter_passes_validation():
    result = Encounter.model_validate(valid_encounter)

    assert result.id == "c2aadfa1-256b-c450-48e9-0a5e44171a14"
    assert result.resourceType == "Encounter"
    assert result.status == "finished"
    assert result.class_.code == "AMB"
    assert result.subject.reference == ("urn:uuid:c2aadfa1-256b-c450-bcd5-442316fa4fe9")
    assert result.period.start.year == 1997


def test_valid_condition_passes_validation():
    result = Condition.model_validate(valid_condition)

    assert result.id == "c2aadfa1-256b-c450-e2a4-42a0880217f0"
    assert result.resourceType == "Condition"
    assert result.clinicalStatus.coding[0].code == "resolved"
    assert result.verificationStatus.coding[0].code == "confirmed"
    assert result.code.coding[0].code == "109838007"


def test_encounter_missing_subject_fails_validation():
    invalid_encounter = valid_encounter.copy()
    invalid_encounter.pop("subject")

    with pytest.raises(ValidationError):
        Encounter.model_validate(invalid_encounter)


def test_condition_missing_code_fails_validation():
    invalid_condition = valid_condition.copy()
    invalid_condition.pop("code")

    with pytest.raises(ValidationError):
        Condition.model_validate(invalid_condition)


def test_valid_patient_passes_validation():
    result = Patient.model_validate(valid_patient)

    assert result.id == "c2aadfa1-256b-c450-bcd5-442316fa4fe9"
    assert result.resourceType == "Patient"
    assert result.name[0].family == "DuBuque211"
    assert result.address[0].state == "BC"


def test_valid_organization_passes_validation():
    result = Organization.model_validate(valid_organization)

    assert result.id == "231f25bb-2bdc-31e6-b187-3e666cb9f8fa"
    assert result.resourceType == "Organization"
    assert result.name == "Primecare Medical Centre"
    assert result.address[0].state == "BC"


def test_valid_practitioner_passes_validation():
    result = Practitioner.model_validate(valid_practitioner)

    assert result.id == "4ac6772e-f4cd-3862-b53c-bb433031afc9"
    assert result.resourceType == "Practitioner"
    assert result.name[0].family == "Schumm995"
    assert result.address[0].state == "BC"


def test_encounter_without_reason_code_passes_validation():
    encounter = valid_encounter.copy()
    encounter.pop("reasonCode")

    result = Encounter.model_validate(encounter)

    assert result.reasonCode is None


def test_condition_without_abatement_datetime_passes_validation():
    condition = valid_condition.copy()
    condition.pop("abatementDateTime")

    result = Condition.model_validate(condition)

    assert result.abatementDateTime is None


def test_patient_missing_name_fails_validation():
    invalid_patient = valid_patient.copy()
    invalid_patient.pop("name")

    with pytest.raises(ValidationError):
        Patient.model_validate(invalid_patient)


def test_organization_missing_name_fails_validation():
    invalid_organization = valid_organization.copy()
    invalid_organization.pop("name")

    with pytest.raises(ValidationError):
        Organization.model_validate(invalid_organization)


def test_practitioner_missing_name_fails_validation():
    invalid_practitioner = valid_practitioner.copy()
    invalid_practitioner.pop("name")

    with pytest.raises(ValidationError):
        Practitioner.model_validate(invalid_practitioner)
