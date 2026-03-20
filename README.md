Here’s a clean, professional **`README.md`** for your project 👇

---

```markdown
# 🚀 Manatal → Ashby Migration Tool

A Python-based data migration tool to transfer candidate data from **Manatal** to **Ashby**, with:

- ✅ SQLite database for tracking progress
- ✅ Resume download & upload support
- ✅ Fault-tolerant logging
- ✅ Resume-safe (can restart anytime)
- ✅ On-demand CSV export

---

## 📁 Project Structure

```

migration-project/
│
├── src/
│   ├── main.py
│   ├── config.py
│   │
│   ├── db/
│   │   ├── database.py
│   │   └── operations.py
│   │
│   ├── api/
│   │   ├── manatal.py
│   │   └── ashby.py
│   │
│   ├── services/
│   │   ├── migration.py
│   │   └── transform.py
│   │
│   └── utils/
│       └── exporter.py
│
├── logs/
├── resumes/
├── .env
├── requirements.txt
└── migration.db

````

---

## ⚙️ Setup

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd candidate-migration
````

---

### 2. Create virtual environment

```bash
python -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows
```

---

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Configure environment variables

Create a `.env` file:

```env
MANATAL_API_KEY=your_manatal_api_key
ASHBY_API_KEY=your_ashby_api_key
PER_PAGE=100
API_SLEEP=1
```

---

## ▶️ Usage

### 🔄 Run Migration

```bash
python -m src.main
```

This will:

* Fetch candidates from Manatal
* Transform data
* Create candidates in Ashby
* Upload resumes (if available)
* Store results in SQLite (`migration.db`)

---

### 📤 Export Data to CSV

```bash
python -m src.main export
```

This will generate:

```
logs/migration_log.csv
```

---

## 🧠 How It Works

1. **Fetch Data**

   * Pull candidates from Manatal API (paginated)

2. **Transform Data**

   * Map Manatal fields → Ashby format

3. **Upload to Ashby**

   * Create candidate
   * Upload resume
   * Attach tags (if implemented)

4. **Store in Database**

   * Each processed candidate is logged in SQLite

5. **Checkpointing**

   * Uses DB to track last processed candidate
   * Safe to stop/restart anytime

---

## 🗄️ Database

SQLite database file:

```
migration.db
```

Table:

```
migration_log
```

Columns:

| Column     | Description              |
| ---------- | ------------------------ |
| manatal_id | Source candidate ID      |
| ashby_id   | Target candidate ID      |
| cv         | Resume upload status     |
| notes      | Notes transferred or not |
| tags       | Tags transferred or not  |
| error      | Error message (if any)   |

---

## 📂 Output Files

| Path                     | Description                |
| ------------------------ | -------------------------- |
| `migration.db`           | Main database              |
| `logs/migration_log.csv` | Exported report (optional) |
| `resumes/`               | Downloaded resumes         |

---

## ⚠️ Notes

* Ensure both APIs are accessible and keys are valid
* Resume URLs must be publicly accessible or authorized
* Tag migration is currently a placeholder (extend as needed)

---

## 🚀 Future Improvements

* Parallel processing (faster migration)
* Retry & exponential backoff
* Progress tracking dashboard
* Docker support
* Unit tests

---

## 🛠️ Troubleshooting

### Common Issues

**1. API Errors**

* Check API keys
* Verify endpoints and permissions

**2. Resume Upload Fails**

* Check file size limits
* Validate file format

**3. Migration Stops**

* Just rerun the script — it resumes automatically

---

## 📄 License

MIT License

---

## 👨‍💻 Author

Your Name

```

---

If you want, I can also:
- add badges (build, version, etc.)
- tailor it for GitHub (with screenshots + demo)
- or make a **super polished open-source version** with contribution guidelines
```
