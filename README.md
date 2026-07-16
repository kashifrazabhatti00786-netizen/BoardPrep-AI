# BoardPrep AI 2.0

BoardPrep AI 2.0 is a production-grade educational SaaS platform designed for Pakistani students preparing for board examinations (specifically Punjab Board pattern). It uses Google's Gemini API integrated with a Flask backend to check answers, analyze topics, and offer examiner-style feedback.

## Features
- **Board-style Answer Evaluation:** Matches content against official Punjab Board rubrics and provides structural/presentation feedback.
- **Interactive AI Topic Analyzer:** Synthesizes expected questions (MCQs, short and long questions) and visual/diagram concepts.
- **Enterprise UI/UX:** Built with Tailwind CSS, GSAP animations, and Three.js 3D elements.
- **Clean Architecture:** Separation of Concerns with Presentation, API, Services, Models, and Repository layers.

## Tech Stack
- **Frontend:** HTML5, Tailwind CSS, ES6+ Javascript, GSAP & ScrollTrigger, Three.js
- **Backend:** Python, Flask, Firebase Firestore, Firebase Admin, Gemini API
- **Authentication:** Firebase Authentication
- **Hosting:** Vercel (Frontend), Render (Backend)

## Running the Application
To start the Flask API locally, execute the command from the root of the project to ensure proper absolute module resolution:
```bash
python -m backend.app
```
To run tests:
```bash
python -m pytest backend/tests/
```
