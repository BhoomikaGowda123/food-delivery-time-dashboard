# Food Delivery Time Analysis Dashboard

An interactive Streamlit dashboard built with Python, Pandas, and Plotly. The sidebar contains global filters; every KPI and graph uses the same filtered dataset, so selecting an option updates the whole dashboard.

## Dashboard features

- Global filters for order type, vehicle type, delivery-person age, rating, and delivery time
- KPI cards: number of filtered deliveries, average time, median time, and average rating
- Delivery-time distribution histogram
- Average delivery time by vehicle type
- Average delivery time by order type
- Delivery-person age versus delivery time scatter plot
- Rating versus delivery time scatter plot
- Correlation heatmap
- Filtered data preview and CSV download

## Files

- `app.py` — Streamlit dashboard application
- `delivery_data.csv` — dataset used by the dashboard
- `requirements.txt` — Python package dependencies

## Run locally

1. Install Python 3.10 or newer.
2. Open a terminal in this project folder.
3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Start the dashboard:

   ```bash
   streamlit run app.py
   ```

5. Streamlit will print a local URL (usually `http://localhost:8501`). Open it in your browser.
dashboard link:https://food-delivery-time-dashboard-cf8dc9kohbfbhappbkibxnw.streamlit.app/

## Upload to GitHub

1. Create a new repository on GitHub, for example `food-delivery-time-dashboard`.
2. Upload `app.py`, `delivery_data.csv`, `requirements.txt`, and `README.md` to the repository.
3. Add a `.gitignore` if you later create a Python virtual environment. Do not upload `.venv/` or `__pycache__/`.

You can also upload the project folder using GitHub's website: open the repository, choose **Add file → Upload files**, and drag the project files into the page.

## Deploy as a live dashboard with Streamlit Community Cloud

1. Push the project to GitHub.
2. Sign in to Streamlit Community Cloud and connect GitHub.
3. Choose the repository and branch, set the main file path to `app.py`, and deploy.
4. Ensure `requirements.txt` and `delivery_data.csv` are in the repository root.

## Notes

- The app expects the CSV to be named exactly `delivery_data.csv` and to be in the same folder as `app.py`.
- The original dataset contains delivery details such as age, ratings, order type, vehicle type, location coordinates, and time taken.
- The app removes rows with missing values in the fields needed for the charts.
