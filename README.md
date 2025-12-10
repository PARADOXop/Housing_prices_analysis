
project /
    ├── dataset/
    │   └── cleaned_housing.csv             # Final cleaned dataset
    |   └── india_housing_prices.csv        # original dataset
    │
    ├── project_report.docx            # Final report of the entire project
    │
    ├── main_code/
    │   ├── requirements.txt               # All required Python libraries
    │   ├── cleaning_transformation_analysis.ipynb   # Cleaning, validation, EDA, transformations
    │   ├── KPI.py                         # Streamlit page for KPIs
    │   └── pages/
    │       └── Dashboard.py               # Streamlit dashboard with all charts
    │
    └── README.md

1.  Dataset is present in dataset/ directory
2.  project report file is project report
3.  main_code directory has all the code
    a.  requirements.txt has all the required library for this project to install all libraries at once in terminal type "pip install -r requirements.txt"
    b.  cleaning, validation, transformation and analysis is in
        cleaning_transformation_analysis.ipynb file
    c.  KPI.py is a streamlit app which gives use KPI page
    d.  pages/Dashboard.py gives us remaining dashboard
4.  to run streamlit app : streamlit run main_code/KPI.py
