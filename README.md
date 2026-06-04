# 📋 Task Manager

A robust and responsive web application built with Python and Django, designed to streamline team workflow, assign roles, allocate tasks, and track progress in one convenient workspace.

## Installation

🚀 Installation & Setup
1. Clone the repository
git clone https://github.com/step-98/task_manager
cd task_manager
2. Create a virtual environment
python3 -m venv venv
source venv/bin/activate   # macOS / Linux
venv\Scripts\activate      # Windows
3. Install dependencies
pip install -r requirements.txt
4. Apply database migrations
python manage.py migrate
5. Run the development server
python manage.py runserver


## ✨ Features

* **Worker Management:** Easily add, edit, or delete worker profiles and assign them to specific positions.
* **Task Delegation:** Create tasks with priorities and deadlines, and assign them to the most suitable team members.
* **Categorization:** Organize work using custom Task Types (e.g., Bug, Feature, Refactoring).
* **Responsive UI:** A modern, mobile-friendly interface built with Bootstrap 5 and Material UI Kit.
* **Dashboard Analytics:** Quick overview of total workers, tasks, positions, and task types on the home page.

## 🛠️ Tech Stack

* **Backend:** Python 3, Django
* **Frontend:** HTML5, CSS3, Bootstrap 5, Material Kit
* **Database:** SQLite 
* **Icons & Fonts:** Font Awesome, Google Material Icons

