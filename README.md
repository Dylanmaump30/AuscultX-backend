# AuscultX Backend

This is the backend of the AuscultX project, an application for processing and analyzing audio files.

## Project Structure

```
.env
.gitignore
src/
    app.py
    audioprocess/
        Audioutils.py
        Butterworth.py
        Hilbert.py
        Mainprocess.py
        Monoaudio.py
    database/
        connection.py
        schemas.py
    errors/
        dberrors.py
    files/
        audios/
    routes/
        audio.py
        user.py
    services/
        audios/
            S3Connect.py
            audio_service.py
        users/
            user_service.py
```

## Installation

1. Clone the repository:

   ```sh
   git clone https://github.com/Dylanmaump30/AuscultX-backend.git
   cd AuscultX-backend
   ```

2. Create a virtual environment and activate it:

   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the dependencies:

   ```sh
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the root of the project with the following variables:
   ```
   USER=<your_user>
   PASSWORD=<your_password>
   CLUSTER=<your_cluster>
   DB=<your_database>
   ACCESS_KEY_ID=<your_access_key_id>
   ACCESS_SECRET_KEY=<your_access_secret_key>
   S3_NAME=<your_s3_bucket_name>
   ```

## Usage

To start the Flask server, run:

```sh
python src/app.py
```

The server will be available at `http://0.0.0.0:5000`.

## Endpoints

### Users

- `POST /users/register`: Register a new user.
- `POST /users/login`: User login.

### Audios

- `POST /audios/upload`: Upload an audio file.
- `GET /audios/results/<audio_id>`: Get the processing results of an audio file.
- `GET /audios/<user_id>`: Get the audios of a user.

## Contributions

Contributions are welcome. Please open an issue or a pull request to discuss any changes you wish to make.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
