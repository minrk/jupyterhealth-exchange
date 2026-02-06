from rest_framework.test import APIClient

from core.models import (
    Patient,
    StudyPatientScopeConsent,
)

from .utils import add_patients, add_patient_to_study, Code


def test_patient_practitioner_can_update_own_consents(hr_study):
    patient_1, patient_2 = add_patients(2, organization=hr_study.organization)
    for patient in (patient_1, patient_2):
        add_patient_to_study(patient, hr_study, consent=False)
    client = APIClient()
    client.force_authenticate(patient_1.jhe_user)
    payload = {
        "study_scope_consents": [
            {
                "study_id": hr_study.id,
                "scope_consents": [
                    {
                        "coding_system": Code.OpenMHealth.value,
                        "coding_code": Code.HeartRate.value,
                        "consented": True,
                    }
                ],
            }
        ]
    }
    response = client.post(
        f"/api/v1/patients/{patient_1.id}/consents",
        data=payload,
        format="json",
    )
    assert response.status_code == 200
    created = StudyPatientScopeConsent.objects.filter(
        study_patient__patient=patient_1,
        scope_code__coding_code=Code.HeartRate.value,
    )
    assert created.count() == 1
    # now test the _other_ patient
    response = client.post(
        f"/api/v1/patients/{patient_2.id}/consents",
        data=payload,
        format="json",
    )
    assert response.status_code == 403
    created = StudyPatientScopeConsent.objects.filter(
        study_patient__patient=patient_2,
        scope_code__coding_code=Code.HeartRate.value,
    )
    assert created.count() == 0


def test_patients_pagination(client, organization):
    n = 25
    existing = Patient.objects.all().count()
    add_patients(n - existing, organization)
    r = client.get("/api/v1/patients", {"page_size": 10})
    assert r.status_code == 200
    response = r.json()
    assert response["count"] == n
    assert len(response["results"]) == 10
    all_patients = response["results"]
    while r.get("next"):
        r = client.get(r["next"])
        assert r.status_code == 200
        assert r["results"]
        all_patients.extend(r["results"])
    assert len(all_patients) == n


def test_patients_fhir_pagination(client, organization):
    n = 25
    existing = Patient.objects.all().count()
    add_patients(n - existing, organization)
    r = client.get("/api/v1/Patient", {"_count": 10})
    assert r.status_code == 200
    response = r.json()
    assert response["total"] == n
    assert len(response["entry"]) == 10
    all_patients = response["results"]
    while r.get("next"):
        r = client.get(r["next"])
        assert r.status_code == 200
        assert r["entry"]
        all_patients.extend(r["results"])
    assert len(all_patients) == n
