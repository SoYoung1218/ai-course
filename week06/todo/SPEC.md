# Todo App Project Specification

## 1. Overview
This project is a minimal Todo management web application designed for simplicity and efficiency, serving as a Minimum Viable Product (MVP).

## 2. Tech Stack
- **Backend**: Python Flask
- **Database**: SQLite
- **Frontend**: Bootstrap (for rapid and clean UI development)

## 3. Core Features
- **CRUD Operations**:
  - **Create**: Add new tasks with details.
  - **Read**: View the list of all tasks.
  - **Update**: Edit existing task details (Title, Description, Due Date, Priority).
  - **Delete**: Remove tasks from the list.
- **Task Status Management**:
  - Toggle completion status (Mark as completed/incomplete).

## 4. Data Model (Todo Item)
Each Todo item will store the following information in the SQLite database:
- `id`: Unique identifier (Primary Key)
- `title`: Title of the task (String)
- `description`: Detailed description (Text)
- `due_date`: Deadline for the task (Date)
- `priority`: Importance level (e.g., Low, Medium, High)
- `is_completed`: Completion status (Boolean)
- `created_at`: Timestamp of task creation (DateTime)

## 5. Functional Requirements
- **User Authentication**: 
  - None. Users can access the application and manage tasks immediately without login.
- **Sorting & Filtering**:
  - **Default Sorting**: Tasks are displayed in descending order of creation (newest first).
  - **Visual Organization**: Completed tasks are automatically moved to the bottom of the list to prioritize active tasks.

## 6. UI/UX Design
- **Framework**: Bootstrap for a responsive and modern design.
- **Layout**:
  - A simple input form for quick task entry.
  - A clean list view where each task displays its key information.
  - Intuitive controls (icons or buttons) for completing, editing, and deleting tasks.
