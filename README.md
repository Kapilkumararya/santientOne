# Multimodal Chatbot

## Project Overview
The Multimodal Chatbot is a comprehensive application designed to handle various tasks, including daily task management, document narration, and retrieval-augmented generation (RAG). It features a backend built with Python and a frontend developed using modern JavaScript frameworks.

## Features
### Backend
- **Daily Tasks Service**: Manages and processes daily tasks.
- **Document Narration Service**: Converts documents into narrated audio.
- **Ingestion Service**: Handles data ingestion and preprocessing.
- **RAG Service**: Implements retrieval-augmented generation for intelligent responses.

### Frontend
- **Interactive UI**: A user-friendly interface for interacting with the chatbot.
- **Modern Design**: Built with React and styled for a seamless user experience.

## Project Structure
```
backend/
  daily_tasks_service.py
  document_narration_service.py
  ingest.py
  main.py
  rag.py
  requirements.txt
  static/
    audio/
  storage/
    vector_db/
      faiss_index/
frontend/
  eslint.config.js
  index.html
  package.json
  README.md
  vite.config.js
  public/
  src/
    App.css
    App.jsx
    index.css
    main.jsx
    assets/
```

## Prerequisites
- Python 3.9 or higher
- Node.js 16 or higher
- FAISS for vector database indexing

## Setup Instructions
### Backend
1. Navigate to the `backend` directory:
   ```bash
   cd backend
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   & .venv\Scripts\Activate.ps1  # For Windows
   source .venv/bin/activate       # For macOS/Linux
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the backend services:
   ```bash
   python main.py
   ```

### Frontend
1. Navigate to the `frontend` directory:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the development server:
   ```bash
   npm run dev
   ```

## Usage
- Access the frontend at `http://localhost:3000`.
- Interact with the chatbot for various tasks such as document narration and task management.

## Contributing
1. Fork the repository.
2. Create a new branch for your feature:
   ```bash
   git checkout -b feature-name
   ```
3. Commit your changes:
   ```bash
   git commit -m "Add new feature"
   ```
4. Push to the branch:
   ```bash
   git push origin feature-name
   ```
5. Create a pull request.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments
- [FAISS](https://github.com/facebookresearch/faiss) for vector database indexing.
- [React](https://reactjs.org/) for the frontend framework.
- [Vite](https://vitejs.dev/) for the build tool.