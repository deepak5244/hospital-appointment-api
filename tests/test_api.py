"""
Comprehensive test suite for Hospital Appointment Management API.
Tests cover Patient API, Doctor API, Appointment API, overlap checking, and error handling.
Target coverage: ≥ 85%
"""
import pytest
from datetime import datetime, timedelta


# ===========================
# Patient API Tests
# ===========================


class TestPatientAPI:
    """Tests for Patient endpoints."""
    
    def test_get_all_patients_empty(self, client):
        """Test retrieving all patients when no patients exist."""
        response = client.get("/patients")
        assert response.status_code == 200
        assert response.json() == []
    
    def test_create_patient_success(self, client):
        """Test successful patient creation."""
        patient_data = {
            "name": "John Doe",
            "email": "john@example.com",
            "phone": "1234567890",
        }
        response = client.post("/patients", json=patient_data)
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == patient_data["name"]
        assert data["email"] == patient_data["email"]
        assert data["phone"] == patient_data["phone"]
        assert "id" in data
    
    def test_create_patient_duplicate_email(self, client):
        """Test that creating a patient with duplicate email fails."""
        patient_data = {
            "name": "John Doe",
            "email": "john@example.com",
            "phone": "1234567890",
        }
        # Create first patient
        response1 = client.post("/patients", json=patient_data)
        assert response1.status_code == 201
        
        # Try to create second patient with same email
        patient_data["name"] = "Jane Doe"
        response2 = client.post("/patients", json=patient_data)
        assert response2.status_code == 400  # Bad request due to duplicate email
        assert "already exists" in response2.json()["detail"].lower()
    
    def test_get_patient_by_id_success(self, client):
        """Test retrieving a patient by ID."""
        patient_data = {
            "name": "John Doe",
            "email": "john@example.com",
            "phone": "1234567890",
        }
        create_response = client.post("/patients", json=patient_data)
        patient_id = create_response.json()["id"]
        
        get_response = client.get(f"/patients/{patient_id}")
        assert get_response.status_code == 200
        data = get_response.json()
        assert data["id"] == patient_id
        assert data["name"] == patient_data["name"]
    
    def test_get_patient_by_id_not_found(self, client):
        """Test retrieving a non-existent patient returns 404."""
        response = client.get("/patients/999")
        assert response.status_code == 404
        assert response.json()["detail"] == "Patient not found"
    
    def test_get_all_patients_multiple(self, client):
        """Test retrieving multiple patients."""
        for i in range(3):
            patient_data = {
                "name": f"Patient {i}",
                "email": f"patient{i}@example.com",
                "phone": f"123456789{i}",
            }
            client.post("/patients", json=patient_data)
        
        response = client.get("/patients")
        assert response.status_code == 200
        assert len(response.json()) == 3


# ===========================
# Doctor API Tests
# ===========================


class TestDoctorAPI:
    """Tests for Doctor endpoints."""
    
    def test_get_all_doctors_empty(self, client):
        """Test retrieving all doctors when no doctors exist."""
        response = client.get("/doctors")
        assert response.status_code == 200
        assert response.json() == []
    
    def test_create_doctor_success(self, client):
        """Test successful doctor creation."""
        doctor_data = {
            "name": "Dr. Smith",
            "specialization": "Cardiology",
        }
        response = client.post("/doctors", json=doctor_data)
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == doctor_data["name"]
        assert data["specialization"] == doctor_data["specialization"]
        assert "id" in data
    
    def test_get_doctor_by_id_success(self, client):
        """Test retrieving a doctor by ID."""
        doctor_data = {
            "name": "Dr. Smith",
            "specialization": "Cardiology",
        }
        create_response = client.post("/doctors", json=doctor_data)
        doctor_id = create_response.json()["id"]
        
        get_response = client.get(f"/doctors/{doctor_id}")
        assert get_response.status_code == 200
        data = get_response.json()
        assert data["id"] == doctor_id
        assert data["name"] == doctor_data["name"]
    
    def test_get_doctor_by_id_not_found(self, client):
        """Test retrieving a non-existent doctor returns 404."""
        response = client.get("/doctors/999")
        assert response.status_code == 404
        assert response.json()["detail"] == "Doctor not found"
    
    def test_get_all_doctors_multiple(self, client):
        """Test retrieving multiple doctors."""
        specializations = ["Cardiology", "Neurology", "Orthopedics"]
        for i, spec in enumerate(specializations):
            doctor_data = {
                "name": f"Dr. {i}",
                "specialization": spec,
            }
            client.post("/doctors", json=doctor_data)
        
        response = client.get("/doctors")
        assert response.status_code == 200
        assert len(response.json()) == 3


# ===========================
# Appointment API Tests
# ===========================


class TestAppointmentAPI:
    """Tests for Appointment endpoints."""
    
    @pytest.fixture
    def setup_data(self, client):
        """Create a patient and doctor for appointment tests."""
        patient_data = {
            "name": "John Doe",
            "email": "john@example.com",
            "phone": "1234567890",
        }
        patient_response = client.post("/patients", json=patient_data)
        patient_id = patient_response.json()["id"]
        
        doctor_data = {
            "name": "Dr. Smith",
            "specialization": "Cardiology",
        }
        doctor_response = client.post("/doctors", json=doctor_data)
        doctor_id = doctor_response.json()["id"]
        
        return patient_id, doctor_id
    
    def test_get_all_appointments_empty(self, client):
        """Test retrieving all appointments when none exist."""
        response = client.get("/appointments")
        assert response.status_code == 200
        assert response.json() == []
    
    def test_create_appointment_success(self, client, setup_data):
        """Test successful appointment creation."""
        patient_id, doctor_id = setup_data
        
        start = datetime.now() + timedelta(days=1)
        end = start + timedelta(hours=1)
        
        appointment_data = {
            "patient_id": patient_id,
            "doctor_id": doctor_id,
            "appointment_start": start.isoformat(),
            "appointment_end": end.isoformat(),
        }
        response = client.post("/appointments", json=appointment_data)
        assert response.status_code == 201
        data = response.json()
        assert data["patient_id"] == patient_id
        assert data["doctor_id"] == doctor_id
        assert "id" in data
    
    def test_create_appointment_nonexistent_patient(self, client, setup_data):
        """Test that creating appointment with non-existent patient fails."""
        _, doctor_id = setup_data
        
        start = datetime.now() + timedelta(days=1)
        end = start + timedelta(hours=1)
        
        appointment_data = {
            "patient_id": 999,
            "doctor_id": doctor_id,
            "appointment_start": start.isoformat(),
            "appointment_end": end.isoformat(),
        }
        response = client.post("/appointments", json=appointment_data)
        assert response.status_code == 400
        assert "not found" in response.json()["detail"]
    
    def test_create_appointment_nonexistent_doctor(self, client, setup_data):
        """Test that creating appointment with non-existent doctor fails."""
        patient_id, _ = setup_data
        
        start = datetime.now() + timedelta(days=1)
        end = start + timedelta(hours=1)
        
        appointment_data = {
            "patient_id": patient_id,
            "doctor_id": 999,
            "appointment_start": start.isoformat(),
            "appointment_end": end.isoformat(),
        }
        response = client.post("/appointments", json=appointment_data)
        assert response.status_code == 400
        assert "not found" in response.json()["detail"]
    
    def test_get_appointment_by_id_success(self, client, setup_data):
        """Test retrieving an appointment by ID."""
        patient_id, doctor_id = setup_data
        
        start = datetime.now() + timedelta(days=1)
        end = start + timedelta(hours=1)
        
        appointment_data = {
            "patient_id": patient_id,
            "doctor_id": doctor_id,
            "appointment_start": start.isoformat(),
            "appointment_end": end.isoformat(),
        }
        create_response = client.post("/appointments", json=appointment_data)
        appointment_id = create_response.json()["id"]
        
        get_response = client.get(f"/appointments/{appointment_id}")
        assert get_response.status_code == 200
        data = get_response.json()
        assert data["id"] == appointment_id
        assert data["patient_id"] == patient_id
        assert data["doctor_id"] == doctor_id
    
    def test_get_appointment_by_id_not_found(self, client):
        """Test retrieving a non-existent appointment returns 404."""
        response = client.get("/appointments/999")
        assert response.status_code == 404
        assert response.json()["detail"] == "Appointment not found"


# ===========================
# Appointment Overlap Tests (Business Rule Validation)
# ===========================


class TestAppointmentOverlapPrevention:
    """Tests for overlapping appointment prevention business rule."""
    
    @pytest.fixture
    def setup_data(self, client):
        """Create a patient and doctor for overlap tests."""
        patient_data = {
            "name": "Jane Smith",
            "email": "jane@example.com",
            "phone": "9876543210",
        }
        patient_response = client.post("/patients", json=patient_data)
        patient_id = patient_response.json()["id"]
        
        doctor_data = {
            "name": "Dr. Jones",
            "specialization": "Neurology",
        }
        doctor_response = client.post("/doctors", json=doctor_data)
        doctor_id = doctor_response.json()["id"]
        
        return patient_id, doctor_id
    
    def test_overlapping_appointment_rejected(self, client, setup_data):
        """Test that overlapping appointments are rejected."""
        patient_id, doctor_id = setup_data
        
        # Create first appointment: 10:00 - 11:00
        base_time = datetime.now() + timedelta(days=1)
        start1 = base_time.replace(hour=10, minute=0, second=0, microsecond=0)
        end1 = start1 + timedelta(hours=1)
        
        appointment1 = {
            "patient_id": patient_id,
            "doctor_id": doctor_id,
            "appointment_start": start1.isoformat(),
            "appointment_end": end1.isoformat(),
        }
        response1 = client.post("/appointments", json=appointment1)
        assert response1.status_code == 201
        
        # Try to create overlapping appointment: 10:30 - 11:30
        start2 = start1 + timedelta(minutes=30)
        end2 = start2 + timedelta(hours=1)
        
        appointment2 = {
            "patient_id": patient_id,
            "doctor_id": doctor_id,
            "appointment_start": start2.isoformat(),
            "appointment_end": end2.isoformat(),
        }
        response2 = client.post("/appointments", json=appointment2)
        assert response2.status_code == 400
        assert "overlapping" in response2.json()["detail"].lower()
    
    def test_adjacent_appointment_allowed(self, client, setup_data):
        """Test that adjacent (non-overlapping) appointments are allowed."""
        patient_id, doctor_id = setup_data
        
        # Create first appointment: 10:00 - 11:00
        base_time = datetime.now() + timedelta(days=1)
        start1 = base_time.replace(hour=10, minute=0, second=0, microsecond=0)
        end1 = start1 + timedelta(hours=1)
        
        appointment1 = {
            "patient_id": patient_id,
            "doctor_id": doctor_id,
            "appointment_start": start1.isoformat(),
            "appointment_end": end1.isoformat(),
        }
        response1 = client.post("/appointments", json=appointment1)
        assert response1.status_code == 201
        
        # Create adjacent appointment: 11:00 - 12:00 (starts exactly when first ends)
        start2 = end1
        end2 = start2 + timedelta(hours=1)
        
        appointment2 = {
            "patient_id": patient_id,
            "doctor_id": doctor_id,
            "appointment_start": start2.isoformat(),
            "appointment_end": end2.isoformat(),
        }
        response2 = client.post("/appointments", json=appointment2)
        assert response2.status_code == 201
    
    def test_same_patient_different_doctors_overlap_allowed(self, client):
        """Test that same patient can have overlapping appointments with different doctors."""
        # Create two doctors
        doctor_ids = []
        for i in range(2):
            doctor_data = {
                "name": f"Dr. {i}",
                "specialization": "General Practice",
            }
            response = client.post("/doctors", json=doctor_data)
            doctor_ids.append(response.json()["id"])
        
        # Create patient
        patient_data = {
            "name": "Multi-Doctor Patient",
            "email": "multi@example.com",
            "phone": "5555555555",
        }
        patient_response = client.post("/patients", json=patient_data)
        patient_id = patient_response.json()["id"]
        
        # Create appointment with first doctor
        base_time = datetime.now() + timedelta(days=1)
        start1 = base_time.replace(hour=10, minute=0, second=0, microsecond=0)
        end1 = start1 + timedelta(hours=1)
        
        appointment1 = {
            "patient_id": patient_id,
            "doctor_id": doctor_ids[0],
            "appointment_start": start1.isoformat(),
            "appointment_end": end1.isoformat(),
        }
        response1 = client.post("/appointments", json=appointment1)
        assert response1.status_code == 201
        
        # Create overlapping appointment with second doctor (should be allowed)
        start2 = start1 + timedelta(minutes=30)
        end2 = start2 + timedelta(hours=1)
        
        appointment2 = {
            "patient_id": patient_id,
            "doctor_id": doctor_ids[1],
            "appointment_start": start2.isoformat(),
            "appointment_end": end2.isoformat(),
        }
        response2 = client.post("/appointments", json=appointment2)
        assert response2.status_code == 201
    
    def test_multiple_overlapping_scenarios(self, client, setup_data):
        """Test various overlap scenarios to ensure correct logic."""
        patient_id, doctor_id = setup_data
        
        base_time = datetime.now() + timedelta(days=2)
        start_base = base_time.replace(hour=9, minute=0, second=0, microsecond=0)
        
        # Create appointment: 09:00 - 10:00
        appointment1 = {
            "patient_id": patient_id,
            "doctor_id": doctor_id,
            "appointment_start": start_base.isoformat(),
            "appointment_end": (start_base + timedelta(hours=1)).isoformat(),
        }
        response1 = client.post("/appointments", json=appointment1)
        assert response1.status_code == 201
        
        # Test case 1: Completely before (08:00 - 09:00) - should succeed
        appointment_before = {
            "patient_id": patient_id,
            "doctor_id": doctor_id,
            "appointment_start": (start_base - timedelta(hours=1)).isoformat(),
            "appointment_end": start_base.isoformat(),
        }
        response = client.post("/appointments", json=appointment_before)
        assert response.status_code == 201
        
        # Test case 2: Completely after (10:00 - 11:00) - should succeed
        appointment_after = {
            "patient_id": patient_id,
            "doctor_id": doctor_id,
            "appointment_start": (start_base + timedelta(hours=1)).isoformat(),
            "appointment_end": (start_base + timedelta(hours=2)).isoformat(),
        }
        response = client.post("/appointments", json=appointment_after)
        assert response.status_code == 201
        
        # Test case 3: Partial overlap at start (08:30 - 09:30) - should fail
        appointment_start_overlap = {
            "patient_id": patient_id,
            "doctor_id": doctor_id,
            "appointment_start": (start_base - timedelta(minutes=30)).isoformat(),
            "appointment_end": (start_base + timedelta(minutes=30)).isoformat(),
        }
        response = client.post("/appointments", json=appointment_start_overlap)
        assert response.status_code == 400


# ===========================
# Error Handling Tests
# ===========================


class TestErrorHandling:
    """Tests for proper error handling and HTTP status codes."""
    
    def test_invalid_patient_email_format(self, client):
        """Test that invalid email format is rejected."""
        patient_data = {
            "name": "John Doe",
            "email": "invalid-email",
            "phone": "1234567890",
        }
        response = client.post("/patients", json=patient_data)
        assert response.status_code == 422
    
    def test_missing_required_field(self, client):
        """Test that missing required fields are rejected."""
        patient_data = {
            "name": "John Doe",
            "email": "john@example.com",
            # Missing phone
        }
        response = client.post("/patients", json=patient_data)
        assert response.status_code == 422
    
    def test_negative_id_validation(self, client):
        """Test that negative IDs in appointment are rejected."""
        appointment_data = {
            "patient_id": -1,
            "doctor_id": 1,
            "appointment_start": datetime.now().isoformat(),
            "appointment_end": (datetime.now() + timedelta(hours=1)).isoformat(),
        }
        response = client.post("/appointments", json=appointment_data)
        assert response.status_code == 422


# ===========================
# Integration Tests
# ===========================


class TestIntegration:
    """Integration tests covering complete workflows."""
    
    def test_complete_appointment_workflow(self, client):
        """Test complete workflow: create patient, doctor, and appointment."""
        # Create patient
        patient_data = {
            "name": "Workflow Patient",
            "email": "workflow@example.com",
            "phone": "1111111111",
        }
        patient_response = client.post("/patients", json=patient_data)
        assert patient_response.status_code == 201
        patient_id = patient_response.json()["id"]
        
        # Create doctor
        doctor_data = {
            "name": "Workflow Doctor",
            "specialization": "General Practice",
        }
        doctor_response = client.post("/doctors", json=doctor_data)
        assert doctor_response.status_code == 201
        doctor_id = doctor_response.json()["id"]
        
        # Create appointment
        start = datetime.now() + timedelta(days=3)
        end = start + timedelta(hours=1)
        appointment_data = {
            "patient_id": patient_id,
            "doctor_id": doctor_id,
            "appointment_start": start.isoformat(),
            "appointment_end": end.isoformat(),
        }
        appointment_response = client.post("/appointments", json=appointment_data)
        assert appointment_response.status_code == 201
        appointment_id = appointment_response.json()["id"]
        
        # Verify all data
        verify_patient = client.get(f"/patients/{patient_id}")
        assert verify_patient.status_code == 200
        
        verify_doctor = client.get(f"/doctors/{doctor_id}")
        assert verify_doctor.status_code == 200
        
        verify_appointment = client.get(f"/appointments/{appointment_id}")
        assert verify_appointment.status_code == 200
        assert verify_appointment.json()["patient_id"] == patient_id
        assert verify_appointment.json()["doctor_id"] == doctor_id
