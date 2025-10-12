import streamlit as st
import sqlite3
import pandas as pd

# --- Database Connection ---
DB_PATH = 'naver_search.db'

@st.cache_resource
def get_db_connection():
    """Creates and returns a connection to the SQLite database."""
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def get_table_names(_conn):
    """Fetches and returns a list of table names from the database."""
    cursor = _conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    return [table[0] for table in cursor.fetchall()]

def get_data_from_table(_conn, table_name, search_query="", page=1, page_size=10):
    """Fetches data from the specified table with search and pagination."""
    offset = (page - 1) * page_size
    query = f"SELECT * FROM {table_name}"
    params = []

    # Search in 'title' and 'description' columns if they exist
    try:
        cursor = _conn.cursor()
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = [info[1] for info in cursor.fetchall()]

        search_clauses = []
        if search_query:
            searchable_cols = [col for col in ['title', 'description'] if col in columns]
            for col in searchable_cols:
                search_clauses.append(f"{col} LIKE ?")
                params.append(f"%{search_query}%")

        if search_clauses:
            query += " WHERE " + " OR ".join(search_clauses)

    except Exception as e:
        st.warning(f"Could not apply search: {e}")


    query += f" LIMIT {page_size} OFFSET {offset}"

    try:
        df = pd.read_sql_query(query, _conn, params=params)
        return df
    except pd.io.sql.DatabaseError as e:
        st.error(f"Error: Query failed. {e}")
        return pd.DataFrame()

def get_total_count(_conn, table_name, search_query=""):
    """Gets the total number of rows in a table, optionally filtered by a search query."""
    query = f"SELECT COUNT(*) FROM {table_name}"
    params = []
    if search_query:
        try:
            cursor = _conn.cursor()
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = [info[1] for info in cursor.fetchall()]

            search_clauses = []
            searchable_cols = [col for col in ['title', 'description'] if col in columns]
            for col in searchable_cols:
                search_clauses.append(f"{col} LIKE ?")
                params.append(f"%{search_query}%")

            if search_clauses:
                query += " WHERE " + " OR ".join(search_clauses)
        except Exception:
            pass # Ignore if search cannot be applied

    cursor = _conn.cursor()
    cursor.execute(query, params)
    return cursor.fetchone()[0]

def reset_pagination():
    st.session_state.page = 1

# --- Streamlit App Layout ---
st.set_page_config(page_title="Naver Search DB Viewer", layout="wide")

st.title("Naver Search Results Viewer")
st.write("This application displays data collected from the Naver Search API, stored in the `naver_search.db` database.")

# --- Main Logic ---
conn = get_db_connection()
table_names = get_table_names(conn)

if not table_names:
    st.warning("No tables found in the database. Please run the data collection script first.")
    st.stop()

# --- Sidebar for Table Selection ---
st.sidebar.title("Categories")
selected_table = st.sidebar.selectbox(
    "Select a category to view:",
    options=table_names,
    format_func=lambda x: x.replace('naver_', '').capitalize(), # Prettify table names
    on_change=reset_pagination
)

# --- Search Input ---
search_query = st.text_input("Search by keyword in title or description:", on_change=reset_pagination)


# --- Display Data for Selected Table ---
if selected_table:
    st.header(f"Data for: {selected_table.replace('naver_', '').capitalize()}")

    # --- Pagination ---
    if 'page' not in st.session_state:
        st.session_state.page = 1

    total_items = get_total_count(conn, selected_table, search_query)
    page_size = 10
    total_pages = (total_items + page_size - 1) // page_size if total_items > 0 else 1

    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("⬅️ Previous"):
            if st.session_state.page > 1:
                st.session_state.page -= 1
    with col3:
        if st.button("Next ➡️"):
            if st.session_state.page < total_pages:
                st.session_state.page += 1
    with col2:
        st.write(f"Page {st.session_state.page} of {total_pages} ({total_items} items)")


    df = get_data_from_table(conn, selected_table, search_query, page=st.session_state.page, page_size=page_size)

    if not df.empty:
        # --- Make links clickable ---
        column_config = {}
        link_cols = ['link', 'originallink', 'bloggerlink', 'cafeurl']
        for col in link_cols:
            if col in df.columns:
                column_config[col] = st.column_config.LinkColumn(
                    label=col,
                    display_text="🔗 Click"
                )

        st.dataframe(df, column_config=column_config, use_container_width=True, hide_index=True)

    else:
        st.info(f"No results found for your query in '{selected_table}'.")

st.sidebar.info(f"Connected to `{DB_PATH}`")
