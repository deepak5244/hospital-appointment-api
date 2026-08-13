# Hospital Appointment Management API

A FastAPI-based REST API for managing hospital patients, doctors, and appointments with comprehensive validation, testing, and CI/CD integration.

## Overview

This application provides a complete appointment management system with the following features:

- **Patient Management**: Create, retrieve, and list patients
- **Doctor Management**: Create, retrieve, and list doctors  
- **Appointment Management**: Create, retrieve, and list appointments
- **Overlap Prevention**: Automatically prevents doctors from having overlapping appointments
- **Database Migrations**: Alembic-based schema management
- **Comprehensive Testing**: 85%+ test coverage with pytest
- **Security Scanning**: Bandit security analysis
- **Code Quality**: Automated linting and formatting
- **Docker Support**: Containerized deployment
- **CI/CD Pipeline**: GitHub Actions workflow for build, test, and deployment

## Technology Stack

- **Framework**: FastAPI
- **ORM**: SQLAlchemy
- **Database**: SQLite (development) / PostgreSQL (production-ready)
- **Migrations**: Alembic
- **Testing**: Pytest with coverage reporting
- **Security**: Bandit
- **Containerization**: Docker
- **CI/CD**: GitHub Actions

## Data Models

### Patient
- `id`: Integer (Primary Key)
- `name`: String (100 chars, required)
- `email`: String (150 chars, unique, required)
- `phone`: String (20 chars, required)

### Doctor
- `id`: Integer (Primary Key)
- `name`: String (100 chars, required)
- `specialization`: String (100 chars, required)

### Appointment
- `id`: Integer (Primary Key)
- `patient_id`: Integer (Foreign Key to Patient)
- `doctor_id`: Integer (Foreign Key to Doctor)
- `appointment_start`: DateTime (required)
- `appointment_end`: DateTime (required)

## API Endpoints

### Patients
- `GET /patients` - Retrieve all patients
- `POST /patients` - Create a new patient
- `GET /patients/{id}` - Retrieve patient by ID

### Doctors
- `GET /doctors` - Retrieve all doctors
- `POST /doctors` - Create a new doctor
- `GET /doctors/{id}` - Retrieve doctor by ID

### Appointments
- `GET /appointments` - Retrieve all appointments
- `POST /appointments` - Create a new appointment
- `GET /appointments/{id}` - Retrieve appointment by ID

## Business Rules

### Overlapping Appointment Prevention
The system prevents doctors from having overlapping appointments. When creating an appointment, the system checks:

```
existing_start < new_end AND existing_end > new_start
```

If this condition is true for any existing appointment for the same doctor, the new appointment is rejected with a 400 error.

## Installation

### Prerequisites
- Python 3.14+
- pip

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd hospital-appointment-api
```

2. Create and activate virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run database migrations:
```bash
alembic upgrade head
```

## Running the Application

### Development
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`
- API Documentation: `http://localhost:8000/docs` (Swagger UI)
- Alternative Docs: `http://localhost:8000/redoc` (ReDoc)

### Production
```bash
gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app
```

## Testing

### Run all tests:
```bash
pytest tests/ -v
```

### Run tests with coverage report:
```bash
pytest tests/ --cov=app --cov-report=html -v
```

### Check coverage threshold (85%):
```bash
coverage report --fail-under=85
```

## Code Quality

### Linting:
```bash
flake8 app tests
```

### Security Scanning:
```bash
bandit -r app
```

## Docker

### Build Docker image:
```bash
docker build -t hospital-api:latest .
```

### Run Docker container:
```bash
docker run -p 8000:8000 hospital-api:latest
```

## CI/CD Pipeline

The GitHub Actions workflow includes:

1. **Linting Gate**: Validates Python code quality using flake8
2. **Test Coverage Gate**: Runs pytest and enforces 85% coverage minimum
3. **Security Gate**: Runs Bandit for security vulnerability detection
4. **Build & Push**: Builds Docker image and pushes to Docker Hub (on main branch)

### Setting up GitHub Actions

To enable Docker Hub publishing:

1. Add GitHub Secrets:
   - `DOCKER_USERNAME`: Your Docker Hub username
   - `DOCKER_PASSWORD`: Your Docker Hub password or token

2. Push to `main` branch to trigger the workflow

## Project Structure

```
hospital-appointment-api/
├── app/
│   ├── models/
│   │   ├── patient.py
│   │   ├── doctor.py
│   │   └── appointment.py
│   ├── schemas/
│   │   ├── patient.py
│   │   ├── doctor.py
│   │   └── appointment.py
│   ├── routers/
│   │   ├── patients.py
│   │   ├── doctors.py
│   │   └── appointments.py
│   ├── services/
│   │   ├── patient_service.py
│   │   ├── doctor_services.py
│   │   └── appointment_service.py
│   ├── database.py
│   ├── main.py
│   └── __init__.py
├── tests/
│   ├── test_api.py
│   └── __init__.py
├── alembic/
│   ├── versions/
│   ├── env.py
│   └── script.py.mako
├── .github/
│   └── workflows/
│       └── ci-cd.yml
├── .bandit
├── Dockerfile
├── alembic.ini
├── requirements.txt
├── README.md
└── hospital.db
```

## Example Usage

### Create a Patient
```bash
curl -X POST "http://localhost:8000/patients" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "1234567890"
  }'
```

### Create a Doctor
```bash
curl -X POST "http://localhost:8000/doctors" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Dr. Smith",
    "specialization": "Cardiology"
  }'
```

### Create an Appointment
```bash
curl -X POST "http://localhost:8000/appointments" \
  -H "Content-Type: application/json" \
  -d '{
    "patient_id": 1,
    "doctor_id": 1,
    "appointment_start": "2026-09-01T10:00:00",
    "appointment_end": "2026-09-01T11:00:00"
  }'
```

## License

MIT License

## Support

For issues, questions, or contributions, please open an issue or submit a pull request.
