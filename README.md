# 📝 TextShare — A Minimal Social Network for Text Posts

TextShare is a simple, lightweight social networking web app that allows users to share short text posts in real time. It is built with a modern Python stack using **Streamlit** for the frontend and **FastAPI** for the backend.

---

## 🚀 Features

* ✍️ Create and share text posts
* 📜 View a live feed of posts
* ⚡ Fast and responsive API with FastAPI
* 🎨 Simple and interactive UI using Streamlit
* 🔌 Easy to extend and customize

---

## 🏗️ Tech Stack

* **Frontend:** Streamlit
* **Backend:** FastAPI
* **Language:** Python 3.9+
* **Server:** Uvicorn

---


## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/textshare.git
cd textshare
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate    # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Running the App

### Start the FastAPI backend

```bash
cd backend
uvicorn main:app --reload
```

Backend will run at:
👉 [http://127.0.0.1:8000](http://127.0.0.1:8000)

API docs available at:
👉 [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

### Start the Streamlit frontend

Open a new terminal:

```bash
cd frontend
streamlit run app.py
```

Frontend will run at:
👉 [http://localhost:8501](http://localhost:8501)

---

## 🔗 API Endpoints (Example)

| Method | Endpoint | Description       |
| ------ | -------- | ----------------- |
| GET    | `/posts` | Get all posts     |
| POST   | `/posts` | Create a new post |

---

## 🧠 Future Improvements

* Likes and comments
* Pagination and search
* Deployment (Docker, cloud hosting)

---

## 🤝 Contributing

Contributions are welcome!

1. Fork the repo
2. Create a new branch
3. Make your changes
4. Submit a pull request

---

## 📄 License

This project is licensed under the MIT License
