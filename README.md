# Developer Survey Analysis

An interactive **Streamlit web application** for analyzing the Stack Overflow Annual Developer Survey. Upload survey data in CSV format and explore comprehensive insights about developer demographics, programming languages, work habits, and job satisfaction across the globe.

## Try It Live
 
**No setup required!** Try the app right now: **[https://bit.ly/4vOCMz5](https://bit.ly/4vOCMz5)**
 
Or deploy it yourself locally (see instructions below).

---

## Features

- **Data Validation** — Automatically checks for required columns and validates data integrity
- **Interactive Data Cleaning** — Converts numeric fields, removes outliers, and handles multi-select responses
- **Four Analysis Dashboards:**
  - **Overview** — Dataset statistics, total respondents, column count, missing values, and preview
  - **Demographics** — Gender distribution, education levels, and age when first coding
  - **Languages** — Most used languages this year, most desired next year, and "most loved" languages
  - **Work & Career** — Average work hours by country, top countries by respondents, job satisfaction, and employment types
- **Publication-Ready Visualizations** — Professional charts, pie charts, histograms, and bar plots
- **Dynamic Filtering** — View insights for countries with 250+ responses or top 15 countries
- **Responsive UI** — Wide layout with tabbed navigation for organized exploration

---

## How the Program Works

### Data Processing Pipeline

1. **Upload CSV** — Paste your Stack Overflow survey CSV file
2. **Column Validation** — App checks for 19 required columns; missing columns trigger an error
3. **Data Extraction** — Extracts only the columns needed for analysis
4. **Data Cleaning:**
   - Converts text fields (`Age1stCode`, `YearsCode`, `YearsCodePro`, `WorkWeekHrs`, `Age`) to numeric
   - Drops invalid age values (outside 10–100 range)
   - Drops invalid work hours (over 140 hours/week)
   - Removes multi-select responses from single-choice fields (Gender)
5. **Analysis & Visualization** — Generates live charts across four tabs

### Required CSV Columns

The app expects these 19 columns in the survey CSV:

```
Country, Age, Gender, EdLevel, UndergradMajor, Hobbyist,
Age1stCode, YearsCode, YearsCodePro, LanguageWorkedWith,
LanguageDesireNextYear, NEWLearn, NEWStuck, Employment, DevType,
WorkWeekHrs, JobSat, JobFactors, NEWOvertime, NEWEdImpt
```

---

## Dashboard Overview

### Tab 1: Overview

| Metric | Description |
|---|---|
| **Total Respondents** | Number of survey responses after cleaning |
| **Columns** | Number of data columns retained |
| **Missing Values** | Total null values across the dataset |
| **Countries** | Unique countries represented |
| **Data Preview** | First 10 rows of cleaned data |
| **Statistical Summary** | Min, max, mean, std dev for numeric columns |

### Tab 2: Demographics

| Chart | Description |
|---|---|
| **Gender Distribution** | Horizontal bar chart of gender breakdown (multi-select responses removed) |
| **Education Level** | Horizontal bar chart showing education level distribution |
| **Age at First Code** | Histogram showing distribution of ages when respondents first coded |

### Tab 3: Languages

**Three Views (selectable via radio buttons):**

| View | Description |
|---|---|
| **Most Used This Year** | Pie chart of top 5 programming languages used in the current year |
| **Most Desired Next Year** | Pie chart of top 5 languages developers want to learn next year |
| **Most Loved** | Pie chart of top 5 languages that appear in both "used" and "desired" categories |

> **Note:** Multi-select columns (`LanguageWorkedWith`, `LanguageDesireNextYear`) are split on semicolons and analyzed individually.

### Tab 4: Work & Career

| Chart | Description |
|---|---|
| **Avg Work Hours by Country** | Top 15 countries sorted by average work hours per week (250+ responses only) |
| **Top 15 Countries** | Bar chart showing respondent count by country |
| **Job Satisfaction** | Horizontal bar chart of satisfaction ratings |
| **Employment Type** | Horizontal bar chart of employment status distribution |

---

## How to Get Survey Data

1. **Download from Stack Overflow:**
   - Visit [Stack Overflow Annual Developer Survey](https://survey.stackoverflow.co/)
   - Download the latest survey results CSV

2. **Or use a sample dataset:**
   - Stack Overflow surveys are available on [Kaggle](https://www.kaggle.com/datasets/stackoverflow/stack-overflow-2024-full-developer-survey) with historical data

3. **Expected File Format:**
   - CSV format with headers in the first row
   - 19 required columns (see above)
   - Can contain additional columns (they will be ignored)

---

## How to Run Locally

### Prerequisites

- **Python 3.8+**
- **pip** or **uv** package manager

### Option 1: Install with pip

1. **Clone or download the project:**

```bash
git clone <repository-url>
cd Developer-Survey-Analysis
```

2. **Create a virtual environment (recommended):**

```bash
python -m venv venv

# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

3. **Install dependencies:**

```bash
pip install streamlit pandas numpy seaborn matplotlib
```

4. **Run the web app:**

```bash
streamlit run webapp.py
```

5. **Open in browser:**
   - Streamlit will display a URL (usually `http://localhost:8501`)
   - Click the link or paste it into your browser

---

### Option 2: Install with uv (Faster & Simpler)

**uv is a fast Python package manager. If you don't have it installed:**

```bash
pip install uv
```

**Then in your project directory:**

1. **Sync dependencies:**

```bash
uv sync
```

2. **Run the web app:**

```bash
uv run streamlit run webapp.py
```

3. **Open in browser:**
   - Follow the URL displayed in the terminal

---

## File Structure

```
Developer-Survey-Analysis/
│
├── webapp.py                    # Streamlit app (entry point)
├── main.py                      # All data processing & visualization functions
│
├── pyproject.toml               # Project metadata (for uv)
├── uv.lock                      # Locked dependencies (for uv)
├── .python-version              # Python version specification
├── .gitignore                   # Git ignore rules
│
└── README.md                    # This file
```

---

## Function Reference

### Data Processing (`main.py`)

| Function | Purpose |
|---|---|
| `get_required_info(raw_data)` | Extracts 19 required columns from raw CSV |
| `convert_numeric(df, column)` | Converts text column to numeric, coercing errors to NaN |
| `drop_incorrect(df, column, max, min)` | Removes rows where column values fall outside min–max range |
| `replace_multiselect(df, column)` | Removes rows with semicolon-separated values (for single-choice fields) |
| `split_multicolumn(series)` | Splits semicolon-separated values into boolean columns (one per option) |

### Visualization (`main.py`)

| Function | Output |
|---|---|
| `plot_hbar(df, column, title)` | Horizontal bar chart (countplot) |
| `plot_bar(df, column, title, total_num)` | Vertical bar chart (top N values) |
| `plot_hist(df, column, title)` | Histogram with 5-year bins |
| `plot_pie(values, labels, title)` | Pie chart with percentages |
| `plot_barh(data, title)` | Horizontal bar chart (for aggregated data) |
| `save_fig(fig)` | Saves matplotlib figure to PNG buffer for Streamlit display |

---

## Technologies Used

- **[Streamlit](https://streamlit.io/)** — Fast, open-source web app framework for data science
- **[Pandas](https://pandas.pydata.org/)** — Data manipulation and analysis
- **[NumPy](https://numpy.org/)** — Numerical computing
- **[Seaborn](https://seaborn.pydata.org/)** — Statistical data visualization (built on Matplotlib)
- **[Matplotlib](https://matplotlib.org/)** — Low-level plotting library
- **[Python 3.8+](https://www.python.org/)** — Programming language

---

## Data Cleaning Notes

- **Age Column:** Rows with age < 10 or > 100 are removed (assumed data entry errors)
- **Work Hours:** Rows with work hours > 140 per week are removed (>20 hours/day is unrealistic)
- **Numeric Conversion:** Fields converted with `errors="coerce"` mean invalid values become NaN but don't break the pipeline
- **Multi-Select Handling:** Columns like `LanguageWorkedWith` use semicolons as delimiters; the `split_multicolumn()` function converts these into multiple boolean columns
- **Single-Choice Multi-Select Removal:** Gender field shouldn't have multiple selections; these rows are marked as NaN by `replace_multiselect()`

---

## Troubleshooting

### "Missing required columns: [...]"
- Check that your CSV has all 19 expected columns
- Column names must match exactly (case-sensitive)
- Download the official Stack Overflow survey CSV if you're not sure

### "No module named 'streamlit'"
- Run `pip install streamlit` or `uv sync`

### Charts not displaying
- The app uses `st.image()` to display matplotlib figures
- Ensure your terminal/IDE supports image output
- Try running in a browser instead of terminal

### Data preview is blank
- Ensure your CSV has data rows after the header
- Check that no rows are being dropped by validation filters

---

## Performance Tips

- **Large datasets (50k+ rows):** Processing may take 5–10 seconds on first load due to visualization rendering
- **Streamlit caching:** The app doesn't cache data (by design) so it reprocesses on every file upload — this ensures fresh analysis
- **Countries with 250+ responses:** The "Avg Work Hours by Country" section only includes countries with enough data to be statistically meaningful

---

## Future Enhancements

- Add caching with `@st.cache_data` for faster re-runs
- Export filtered data and charts to PDF
- Add time-series comparison (if multiple survey years are uploaded)
- Interactive filtering by age range, years of experience, or country
- Correlation analysis between job satisfaction and other variables

---

## Notes

- The app is **read-only** — it doesn't modify your CSV or store data
- All processing happens in memory; data is cleared when the browser tab is closed
- Charts are rendered at 120 DPI for clarity in the web interface
- The app uses `bbox_inches="tight"` to prevent label clipping in visualizations

---

## Author

Muhammad Awais Tariq

---

## References

- **Stack Overflow Survey:** https://survey.stackoverflow.co/
- **Survey Data on Kaggle:** https://www.kaggle.com/datasets/stackoverflow/stack-overflow-2024-full-developer-survey
- **Streamlit Docs:** https://docs.streamlit.io/
- **Pandas Docs:** https://pandas.pydata.org/docs/
- **Seaborn Docs:** https://seaborn.pydata.org/

---

If you like this project, consider giving it a star ⭐