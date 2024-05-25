# aiping-l2

## Description
AIPIPING L2 is a FastAPI-based application that provides travel recommendations using OpenAI's API.


## Project Structure
- `app/main.py`: FastAPI application setup.
- `app/utils/make_request.py`: Utility functions for making HTTP requests.
- `pyproject.toml`: Project dependencies and settings.
- `deployments/Dockerfile`: Docker configuration.

## Configuration
- `app/config/config.py`: Configuration settings for the application.

## License
MIT License

## Installation

### Prerequisites
- Python 3.11
- Poetry

### Steps
1. Update and install Poetry:
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

2. Install dependencies:
```bash
poetry install
```

3. Activate the virtual environment:
```bash
poetry shell
```

4. Set the OpenAI API key:
```bash
export OPENAI_API_KEY=API_KEY
```

5. Run the application:
```bash
uvicorn app.main:app --reload --port 3000 --host 0.0.0.0
```

6. Access this URL on your browser: [http://0.0.0.0:3000/api/v1/docs](http://0.0.0.0:3000/api/v1/docs)

### Build and Run Docker Compose:
```bash
export OPENAI_API_KEY=API_KEY
docker-compose -f deployments/docker-compose.yml up -d
```

### Running unittest
```bash
pytest tests
```