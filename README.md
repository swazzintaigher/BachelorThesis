# Medical Records Management System

This Flask-based web application is designed for managing medical records as part of a thesis project. The system provides functionalities for user authentication, patient registration, and the ability to upload and associate medical images with patient records. It also allows users to view patient information along with details of associated images and lesion classifications.

## Features

- **User Authentication:** Secure user login and registration functionality.
  
- **Patient Management:** Add, view, and manage patient records with basic information.
  
- **Image Upload:** Upload medical images and associate them with patient records.

- **Lesion Details:** View lesion details, including size, location, and automatic/manual classifications.

## Technologies Used

- **Flask:** A Python web framework used for building the application.
  
- **PostgreSQL:** Database management system for storing user and patient data.

- **Flask-WTF, Flask-Uploads:** Libraries for handling web forms and file uploads in Flask.

- **Pillow:** Python Imaging Library used for image processing.

## Usage

1. **Installation:**
   - Clone the repository.
   - Install dependencies using `pip install -r requirements.txt`.

2. **Database Setup:**
   - Create a PostgreSQL database.
   - Update the database connection details in the `connect_db()` function.

3. **Run the Application:**
   - Execute `python app.py` to start the Flask development server.
   - Access the application in your web browser at `http://localhost:5000`.

4. **Contribution:**
   - Fork the repository, make your changes, and submit a pull request.
   - Follow the contribution guidelines specified in the repository.

## Documentation

For detailed instructions on installation, configuration, and usage, refer to the [documentation](link_to_documentation).

## License

This project is licensed under the [MIT License](LICENSE).

---

Feel free to customize this README based on the specific details of your project, and don't forget to provide a link to any documentation or license information.
