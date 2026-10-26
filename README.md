# NOVA — Retail Analytics

NOVA is a retail analytics application that lets users explore retail data using natural-language questions, review query results, and visualize insights through interactive charts. It combines a Streamlit frontend, a FastAPI backend, and a SQLite database in a clean, monochrome interface.

## Features

- **Natural-language analytics:** Ask business questions in plain English and explore the returned results.
- **Interactive visualizations:** View supported results as bar, line, or pie charts.
- **NOVA Assistant:** Use the floating assistant for help and to open supported questions directly in Explore.
- **Topics & Guide:** Browse example questions and explanations for common retail analytics topics.
- **SQL-backed analysis:** Review query results and generated SQL where available.
- **Minimal interface:** Black, white, and grey styling for a focused analytics experience.

## Tech Stack

- **Frontend:** Streamlit
- **Backend:** FastAPI
- **Database:** SQLite
- **Charts:** Plotly
- **Language:** Python

## Project Structure

```text
NOVA_Business_Analytics/
├── app/                 # FastAPI backend and query logic
├── frontend/            # Streamlit user interface
├── database/            # SQLite database and schema
├── data/                # Supporting data files, if included
├── .streamlit/          # Streamlit configuration, if included
├── requirements.txt     # Python dependencies
└── README.md
```

The exact files and folders may vary slightly by version.

## Prerequisites

- Python
- The project files and SQLite database included with your copy of NOVA

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/NOVA-Business-Analytics.git
cd NOVA-Business-Analytics
```

Replace `YOUR_USERNAME` with your GitHub username.

### 2. Create and activate a virtual environment

**Windows PowerShell**

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

### 4. Start the backend

In a terminal at the project root:

```powershell
python -m uvicorn app.main:app --reload
```

The API should be available at `http://127.0.0.1:8000`. If enabled, interactive API documentation is available at `http://127.0.0.1:8000/docs`.

### 5. Start the frontend

Open a **second terminal** at the project root and activate the same environment:

```powershell
.\venv\Scripts\Activate.ps1
python -m streamlit run frontend\streamlit_app.py
```

Open the local URL printed by Streamlit, typically `http://localhost:8501`.

Keep both terminals running while using the app.

## How to Use

1. Open NOVA in your browser.
2. Enter a supported business question in **Explore**, or choose an example from **Topics & Guide**.
3. Review the returned results and generated SQL, where available.
4. Switch between bar, line, and pie charts when the result supports visualization.
5. Use the floating **N.** assistant for help or to open supported example questions.

## Example Questions

Available questions depend on the queries supported by the current version. Examples may include:

- What is the total revenue?
- Show monthly revenue.
- Which products have the highest sales?
- Which cities perform best?
- How many orders are there?
- What is the average order value?
- Show the distribution by payment method.

## Troubleshooting

### `uvicorn` or `streamlit` is not recognized

Activate the project's virtual environment and run:

```powershell
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload
python -m streamlit run frontend\streamlit_app.py
```

### The backend root shows `{"detail":"Not Found"}`

The API root route may not be defined in the version you are running. Check `http://127.0.0.1:8000/docs` or a configured health endpoint to confirm the API is available. A root-page response is not required for the Streamlit frontend to communicate with the backend.

### The frontend cannot connect to the backend

- Confirm the backend terminal is still running.
- Confirm the backend is listening at `http://127.0.0.1:8000`.
- Check that the API base URL configured in the frontend matches the backend address.

### The database cannot be found

- Confirm `database/online_retail.db` exists.
- Check whether the backend expects a relative or absolute database path.
- Run the application from the project root unless your code specifies otherwise.

## Security and Repository Notes

- **Do not commit API keys, passwords, or `.env` files.**
- Do not upload `venv/`, `.venv/`, or Python cache files.
- Check the database's licensing and redistribution permissions before publishing it publicly.
- If the database is excluded from GitHub, document how users can obtain or generate it.

## Future Improvements

Possible extensions include broader natural-language query support, more robust query validation, additional chart and filtering options, exportable reports, and automated tests.

## License

No license has been specified yet. Add a license file if you intend to define how others may use, modify, and redistribute this project.


A Business Analytics Project done by 
Krishna Reddy PRN:25030421047
Ananth Teja   PRN:25030422119
Manu Kaul     PRN:25030422069
