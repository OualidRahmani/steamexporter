# Steam Library Exporter

A modern, modular Python pipeline that retrieves your entire Steam library, enriches it with real-time pricing and metadata from the Steam Store API, and exports it into highly structured formats.

## Features

* **Complete Library Retrieval:** Resolves vanity URLs and fetches your entire Steam game collection.
* **Store Metadata Enrichment:** Pulls in live pricing, discount percentages, developers, and publishers.
* **Smart API Caching:** Implements local JSON caching (`cache/`) and automated rate-limit handling (`tqdm`) to respect Steam's strict API limits (200 requests/5 min) and speed up subsequent runs.
* **Multi-Format Export:**
* **CSV:** A clean, flat file of your library (`output/library.csv`).
* **Excel Workbook:** A multi-sheet `xlsx` file containing your library, calculated stats, top developers, and top publishers.
* **SQLite Database:** A fully structured local database (`library.db`) managed via SQLAlchemy ORM for complex queries.



## Quick Start

### 1. Prerequisites

* Python 3.10+
* A Steam API Key (Get one [here](https://steamcommunity.com/dev/apikey))
* A public Steam Profile

### 2. Installation

Clone the repository and navigate into the project directory:

```bash
git clone https://github.com/yourusername/steamexporter.git
cd steamexporter

```

Create and activate a virtual environment:

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux/macOS
python3 -m venv .venv
source .venv/bin/activate

```

Install the required dependencies from requirements.txt:

```bash
pip install -r requirements.txt

```

### 3. Configuration (Environment Variables)

For security, API keys are not stored in this repository. You must create your own local configuration file.

1. Locate the `.env.example` file in the root directory.
2. Duplicate it and rename the copy to `.env`.
3. Open `.env` and add your Steam credentials:

```env
STEAM_API_KEY=your_api_key_here
STEAM_VANITY_URL=your_custom_profile_url_name

```

### 4. Usage

**Run the Exporter Pipeline:**
Execute the main script to fetch, enrich, and export your data.

```bash
python steam_export.py

```

*Note: If you have a large library, the script will automatically pause to respect Steam's rate limits. Do not close the terminal; it will resume automatically.*

**Query the Database:**
Once the pipeline finishes, a `library.db` file will be generated.

## Project Structure

* `steam_export.py`: The main execution pipeline.
* `steam_api.py` / `steam_store.py`: API clients for handling network requests and caching.
* `models.py`: Domain models (Dataclasses) for game objects.
* `mappers.py`: Logic for translating raw JSON into Python objects.
* `exporter.py`: Handles CSV and Excel generation using `openpyxl`.


* `database.py`: SQLAlchemy setup, schema definition, and SQLite injection logic.

## Troubleshooting

* **`PermissionError: [Errno 13]`**: If the script crashes while saving the `.xlsx` file, ensure you do not have `output/library.xlsx` open in Microsoft Excel or another spreadsheet viewer.
* **Missing Games**: Ensure your Steam profile's "Game Details" privacy setting is set to "Public".

---