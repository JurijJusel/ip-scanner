# IP Scanner

A FastAPI-based IP scanner that integrates with AbuseIPDB and VirusTotal
to provide comprehensive IP address intelligence and threat analysis.

## Features

- **IP Address Validation**: Validates IP addresses and resolves domain names to IPs
- **AbuseIPDB Integration**: Check IP reputation and abuse reports from AbuseIPDB
- **VirusTotal Integration**: Analyze IP addresses against VirusTotal's threat intelligence database
- **Domain Resolution**: Automatically convert domain names to IP addresses for analysis
- **RESTful API**: Clean FastAPI endpoints for easy integration
- **Structured Data**: Pydantic models for consistent data validation and serialization

## API Endpoints

### AbuseIPDB
```
GET /abuseipdb/{ip_or_domain}
```
Returns abuse information for the specified IP address or domain.

### VirusTotal
```
GET /virustotal/{ip_or_domain}
```
Returns threat intelligence data from VirusTotal for the specified IP address or domain.

## Installation

### Prerequisites
- Python 3.12 or higher
- API keys for AbuseIPDB and VirusTotal

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd ip-scanner
```

2. Create a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
uv add -r pyproject.toml
```

4. Set up environment variables:
Create a `.env` file in the project root:
```env
ABUSEIPDB_API=your_abuseipdb_api_key
VIRUSTOTAL_API=your_virustotal_api_key
```

## Usage

### Running the Application

Start the FastAPI server:
```bash
python main.py
```

The server will start on `http://localhost:8000`

### API Documentation

Once the server is running, visit:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

### Example Requests

#### Check an IP with AbuseIPDB
```bash
curl http://localhost:8000/abuseipdb/8.8.8.8
```

#### Check a domain with VirusTotal
```bash
curl http://localhost:8000/virustotal/google.com
```

## Project Structure

```
ip-scanner/
├── main.py                 # FastAPI application entry point
├── config.py               # Configuration constants
├── routers/                # API route handlers
│   ├── abuseip_router.py   # AbuseIPDB endpoints
│   └── virustotal_router.py # VirusTotal endpoints
├── services/               # Business logic
│   ├── service_abuseip.py  # AbuseIPDB API integration
│   └── service_virustotal.py # VirusTotal API integration
├── models/                 # Pydantic data models
│   ├── abuseip_model.py    # AbuseIPDB response models
│   └── virustotal_model.py # VirusTotal response models
├── utils/                  # Utility functions
│   ├── clean_domain_ip.py  # Domain to IP resolution
│   └── validators.py       # IP validation utilities
├── .env                    # Environment variables (not tracked)
├── .gitignore              # Git ignore rules
├── pyproject.toml          # Project configuration
└── README.md               # This file
```

## API Keys Setup

### AbuseIPDB
1. Sign up at [AbuseIPDB](https://www.abuseipdb.com/)
2. Get your API key from the account dashboard
3. Add it to your `.env` file as `ABUSEIPDB_API`

### VirusTotal
1. Sign up at [VirusTotal](https://www.virustotal.com/)
2. Get your API key from the profile section
3. Add it to your `.env` file as `VIRUSTOTAL_API`

## Dependencies

- **FastAPI**: Modern, fast web framework for building APIs
- **Pydantic**: Data validation using Python type annotations
- **Requests**: HTTP library for making API calls
- **Python-dotenv**: Load environment variables from .env file
- **Uvicorn**: ASGI server for running FastAPI applications

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
