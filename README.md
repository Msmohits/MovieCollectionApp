# MovieCollectionApp

Welcome to the MovieCollectionApp! This project is a Django-based application for managing and organizing movie collections.

For detailed documentation, refer to the [project document](https://docs.google.com/document/d/1IYGW6CZB5nQ3DmNgBotI10h0bnGep1r5g2D_ZRaFMDc/).

## Setup and Installation

1. **Create a new Django project:**

    ```bash
    django-admin startproject MovieCollectionApp
    cd MovieCollectionApp
    ```

2. **Create a new Django app:**

    ```bash
    django-admin startapp moviecollection
    ```

3. **Install required packages:**

    ```bash
    pip install -r requirement.txt
    ```

4. **Format code with Black:**

    ```bash
    black .
    ```

5. **Run migrations:**

    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

6. **Create a superuser:**

    ```bash
    python manage.py createsuperuser
    ```

7. **Set environment variables for superuser credentials:**

    ```bash
    export username='iNd3jDMYRKsN1pjQPMRz2nrq7N99q4Tsp9EY9cM0'
    export password='Ne5DoTQt7p8qrgkPdtenTK8zd6MorcCR5vXZIJNfJwvfafZfcOs4reyasVYddTyXCz9hcL5FGGIVxw3q02ibnBLhblivqQTp4BIC93LZHj4OppuHQUzwugcYu7TIC5H1'
    ```

8. **Run the development server:**

    ```bash
    uvicorn MovieCollectionApp.asgi:application --host 0.0.0.0 --port 8000 --reload
    ```

    Or

    ```bash
    python manage.py runserver
    ```

## Running Tests

- **Run all test cases:**

    ```bash
    pytest
    ```

- **Run a specific test case:**

    ```bash
    pytest moviecollection/tests/test_register.py::test_users_view
    ```

- **Run test cases with debugger:**

    ```bash
    python -m pdb -m pytest moviecollection/tests/test_collection.py
    ```

## Contributing

Feel free to submit issues or pull requests if you would like to contribute to this project.
