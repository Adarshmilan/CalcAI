# CalcAI Project Report

## 1. Project Overview

**CalcAI** is an intelligent, AI-powered calculator application that allows users to solve mathematical problems by simply drawing them on a digital canvas. The application leverages advanced computer vision and generative AI to interpret handwritten equations, graphical problems, and even abstract concepts, providing solutions in real-time.

The project is divided into two main components:

- **Backend (`calcai-be`):** A Python-based API that handles image processing and AI interaction.
- **Frontend (`calcai-fe`):** A React-based web interface that provides a drawing canvas and displays results.

---

## 2. Architecture & Workflow

### How it Works

1.  **User Interaction:** The user draws a mathematical expression, equation, or graphical problem on the frontend canvas.
2.  **Data Capture:** The frontend captures the drawing as an image (base64 encoded).
3.  **API Request:** The image, along with any user-defined variables, is sent to the backend API endpoint (`/calculate`).
4.  **AI Processing:**
    - The backend receives the image and forwards it to **Google's Gemini 2.5 Flash** model.
    - A specialized prompt instructs the AI to analyze the image based on PEMDAS rules and specific problem types (simple expressions, equations, variable assignments, graphical problems, or abstract concepts).
5.  **Response Parsing:** The AI returns the solution in a structured format, which the backend parses.
6.  **Result Display:** The backend sends the result back to the frontend. The frontend renders the mathematical solution using **MathJax** and allows the user to drag the solution text around the canvas.

---

## 3. Component Details

### Backend (`calcai-be`)

The backend is built using **FastAPI**, a modern, high-performance web framework for building APIs with Python.

- **Entry Point:** `main.py` initializes the FastAPI app, sets up CORS middleware (to allow frontend communication), and includes the calculator router.
- **API Route:** `apps/calculator/route.py` defines the POST `/calculate` endpoint. It decodes the base64 image and calls the utility function.
- **Core Logic:** `apps/calculator/utils.py` contains the `analyze_image` function. This function:
  - Configures the Google Generative AI client.
  - Constructs a detailed prompt defining 5 types of solvable problems.
  - Sends the image and prompt to the Gemini model.
  - Parses the text response into a Python dictionary/list using `ast.literal_eval`.
- **Configuration:** `constants.py` and `schema.py` manage environment variables (like API keys) and Pydantic models for data validation.

### Frontend (`calcai-fe`)

The frontend is a Single Page Application (SPA) built with **React** and **Vite**.

- **Drawing Canvas:** Located in `src/screens/home/index.tsx`, it uses an HTML5 `<canvas>` element to capture user input.
- **State Management:** Uses React `useState` and `useRef` to manage drawing state, colors, and results.
- **API Communication:** Uses **Axios** to send POST requests to the backend.
- **Math Rendering:** Integrates **MathJax** to render complex mathematical expressions (LaTeX) returned by the backend.
- **UI Components:**
  - **Mantine:** Used for UI elements like Color Swatches.
  - **Tailwind CSS:** Used for styling the application.
  - **React Draggable:** Allows the rendered math solutions to be moved around the screen.

---

## 4. Technologies & Packages Used

### Backend Technologies

- **Language:** Python
- **Framework:** FastAPI
- **Server:** Uvicorn
- **AI Model:** Google Gemini 2.5 Flash (`google-generativeai`)
- **Image Processing:** Pillow (PIL)
- **Utilities:** `python-dotenv` (implied for env vars)

### Frontend Technologies

- **Language:** TypeScript
- **Framework:** React (v19)
- **Build Tool:** Vite
- **Styling:** Tailwind CSS (v4), PostCSS
- **UI Libraries:**
  - `@mantine/core`, `@mantine/hooks`
  - `@radix-ui/react-slot`
  - `lucide-react` (Icons)
  - `class-variance-authority`, `clsx`, `tailwind-merge` (Utility for classes)
- **Functional Libraries:**
  - `axios` (HTTP Requests)
  - `react-draggable` (Drag & Drop)
  - `mathjax` (Math Rendering)
  - `react-router-dom` (Routing)
- **Linting:** ESLint, TypeScript-ESLint

---

## 5. Working Process Summary

The entire system operates as a seamless loop:
**Draw -> Capture -> Analyze (AI) -> Solve -> Render**

The user draws on the screen -> The app "sees" the drawing -> The AI "thinks" about the math problem -> The system returns the calculated answer -> The user sees the result overlaid on their canvas.
