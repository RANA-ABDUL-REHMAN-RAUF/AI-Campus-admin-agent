# backend/README.md

# Campus Administration Agent - Backend

This is the backend component of the Campus Administration Agent project, built using FastAPI. This application serves as the server-side logic for managing campus administration tasks.

## Project Structure

- `app/`: Contains the main application code.
  - `main.py`: Entry point of the FastAPI application.
  - `api/`: Contains the API routes.
    - `routes.py`: Defines the API endpoints and links them to service methods.
  - `models/`: Contains data models for request validation and response serialization.
    - `models.py`: Defines the data models using Pydantic.
  - `services/`: Contains business logic and data processing functions.
    - `service.py`: Implements the core functionality of the application.
  - `utils/`: Contains utility functions for common tasks.
    - `helpers.py`: Provides helper functions used throughout the application.

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd campus-admin-agent/backend
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   ```

3. Activate the virtual environment:
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```
     source venv/bin/activate
     ```

4. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Running the Application

To start the FastAPI application, run the following command:
```
uvicorn app.main:app --reload
```

The application will be accessible at `http://127.0.0.1:8000`.

## API Documentation

The automatically generated API documentation can be found at `http://127.0.0.1:8000/docs`.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.