import streamlit as st
import pandas as pd
from datetime import datetime

from core.schema import JobRecord
from core.enhance import bulk_enhance
from core.validate import validate_dataset
from core.io import load_json, save_json_str, generate_changelog, deduplicate_data

# --- CONFIG ---
st.set_page_config(
    page_title="Job Description Architect",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- STATE MANAGEMENT ---
if "data" not in st.session_state:
    st.session_state["data"] = [] # The working list of dicts
if "original_data" not in st.session_state:
    st.session_state["original_data"] = [] # For diffing
if "validation_issues" not in st.session_state:
    st.session_state["validation_issues"] = []
if "changelog" not in st.session_state:
    st.session_state["changelog"] = []
if "file_loaded" not in st.session_state:
    st.session_state["file_loaded"] = False

st.title("Job Description Architect")
st.markdown(
    "Upload or load a dataset, then filter, enhance, validate, and export job descriptions."
)

# --- SIDEBAR ---
st.sidebar.title("Job Description Architect 🏗️")

# 1. File Loader
uploaded_file = st.sidebar.file_uploader("Load Job Descriptions (JSON)", type=["json"])
load_default = st.sidebar.button("Load Default (./data/job_descriptions2.json)")

def load_data_handler(file_obj):
    try:
        raw_data = load_json(file_obj)
        st.session_state["data"] = raw_data
        st.session_state["original_data"] = [r.copy() for r in raw_data] # Deep copy for diff
        st.session_state["file_loaded"] = True
        st.session_state["changelog"] = []
        run_validation()
        st.sidebar.success(f"Loaded {len(raw_data)} records.")
    except Exception as e:
        st.sidebar.error(f"Error loading file: {e}")

if uploaded_file:
    # Only reload if content changes to prevent reset on interaction
    # Hash file content roughly or just reload on user action. 
    # For simplicity in Streamlit, we rely on the uploader state.
    if not st.session_state["file_loaded"]:
        load_data_handler(uploaded_file)

if load_default:
    try:
        with open("./data/job_descriptions2.json", "r", encoding="utf-8") as f:
            load_data_handler(f)
    except FileNotFoundError:
        st.sidebar.error("Default file not found.")

if not st.session_state["file_loaded"]:
    st.info("Please upload a JSON file or load the default dataset to begin.")
    st.stop()

# 2. Operations
st.sidebar.markdown("---")
st.sidebar.subheader("Operations")

if st.sidebar.button("✨ Auto-Enhance All"):
    # Enhance narrative fields while preserving original record structure/field names
    try:
        records_objs = []
        indices = []

        # Build list of JobRecord objects and track their indices
        for idx, r in enumerate(st.session_state["data"]):
            try:
                records_objs.append(JobRecord(**r))
                indices.append(idx)
            except Exception:
                # If data is currently invalid schema, skip enhancement for that record
                continue

        enhanced_objs, count = bulk_enhance(records_objs)

        # Start from the existing data and merge enhanced narrative fields back in
        new_data = list(st.session_state["data"])
        narrative_fields = [
            "key_duties_responsibilities",
            "position_complexity",
            "organizational_impact",
            "career_progression_path",
        ]

        for rec_index, enhanced_rec in zip(indices, enhanced_objs):
            base = dict(new_data[rec_index])  # copy existing record to preserve all fields
            enhanced_dict = enhanced_rec.model_dump()

            # Update only the narrative fields from the enhanced record
            for field in narrative_fields:
                if field in enhanced_dict and enhanced_dict[field] is not None:
                    base[field] = enhanced_dict[field]

            # Ensure Workforce Planner-compatible jobDescription is present
            if not base.get("jobDescription"):
                parts = []
                summary = base.get("position_summary") or base.get("positionSummary")
                if summary and str(summary).strip():
                    parts.append(str(summary).strip())
                duties = base.get("key_duties_responsibilities")
                if duties and str(duties).strip():
                    parts.append(str(duties).strip())
                if parts:
                    base["jobDescription"] = "\n\n".join(parts)

            new_data[rec_index] = base

        # Update state with merged records (all original fields preserved)
        st.session_state["data"] = new_data

        # Log entry
        st.session_state["changelog"].append({
            "timestamp": datetime.now().isoformat(),
            "action": "bulk_enhance",
            "records_modified": count,
        })

        st.toast(f"Enhanced {count} records!", icon="✨")
        run_validation()  # Re-validate after change
        st.rerun()
    except Exception as e:
        st.error(f"Enhancement failed: {e}")

if st.sidebar.button("🧹 Deduplicate"):
    original_len = len(st.session_state["data"])
    st.session_state["data"] = deduplicate_data(st.session_state["data"])
    new_len = len(st.session_state["data"])
    st.sidebar.info(f"Removed {original_len - new_len} duplicates.")
    st.rerun()

# 3. Filters
st.sidebar.markdown("---")
st.sidebar.subheader("Filters")
df = pd.DataFrame(st.session_state["data"])

# Helper to handle missing columns in empty dataset
filter_families = []
filter_depts = []
if not df.empty and "careerFamily" in df.columns:
    filter_families = st.sidebar.multiselect("Career Family", options=df["careerFamily"].unique())
if not df.empty and "department" in df.columns:
    filter_depts = st.sidebar.multiselect("Department", options=df["department"].unique())

search_term = st.sidebar.text_input("Search (Title/Desc)")

# --- MAIN LOGIC ---

def run_validation():
    _, issues = validate_dataset(st.session_state["data"])
    st.session_state["validation_issues"] = [i.to_dict() for i in issues]

# Apply Filters
filtered_df = df.copy()
if not filtered_df.empty:
    if filter_families:
        filtered_df = filtered_df[filtered_df["careerFamily"].isin(filter_families)]
    if filter_depts:
        filtered_df = filtered_df[filtered_df["department"].isin(filter_depts)]
    if search_term:
        # Simple case-insensitive string match across key text columns
        search_cols = [
            c
            for c in [
                "positionTitle",
                "key_duties_responsibilities",
                "position_complexity",
            ]
            if c in filtered_df.columns
        ]
        if search_cols:
            mask = filtered_df[search_cols].apply(
                lambda row: row.astype(str).str.contains(search_term, case=False).any(),
                axis=1,
            )
            filtered_df = filtered_df[mask]

# --- UI LAYOUT ---

tab_editor, tab_valid, tab_diff, tab_export = st.tabs(["📝 Data Editor", "✅ Validation", "⚖️ Diff View", "💾 Export"])

with tab_editor:
    st.markdown(f"**Showing {len(filtered_df)} of {len(df)} records**")
    
    if not filtered_df.empty:
        # Data Editor
        edited_df = st.data_editor(
            filtered_df,
            num_rows="dynamic",
            use_container_width=True,
            key="main_editor"
        )
        
        # Detailed View Logic
        st.markdown("### Detail Editor")

        selected_index = 0
        editor_state = st.session_state.get("main_editor")
        if isinstance(editor_state, dict):
            selection = editor_state.get("selection")
            if isinstance(selection, dict):
                rows = selection.get("rows")
                if isinstance(rows, list) and rows:
                    selected_index = min(rows[0], len(edited_df) - 1)
                elif isinstance(rows, dict) and rows:
                    first_key = sorted(rows.keys())[0]
                    selected_index = min(first_key, len(edited_df) - 1)
        
        # Get the actual record from the filtered view
        try:
            # We need to map the filtered index back to the real data index if we want to save efficiently
            # For MVP, we just grab the record from the edited_df display
            record_to_edit = edited_df.iloc[selected_index].to_dict()
            
            col1, col2 = st.columns(2)
            with col1:
                new_title = st.text_input("Position Title", record_to_edit.get("positionTitle", ""))
                new_dept = st.text_input("Department", record_to_edit.get("department", ""))
                new_family = st.selectbox("Career Family", options=[record_to_edit.get("careerFamily")] + [cf for cf in ["Leadership & Management", "Administrative Support", "General"] if cf != record_to_edit.get("careerFamily")])
            
            with col2:
                st.markdown("**Generated Content**")
                new_duties = st.text_area("Duties", record_to_edit.get("key_duties_responsibilities", ""), height=150)
                new_complex = st.text_area("Complexity", record_to_edit.get("position_complexity", ""), height=100)
            
            # Note: True bi-directional binding between detailed view and data_editor 
            # in Streamlit requires careful state management (callbacks). 
            # For this Click-to-Run MVP, the Data Editor above is the primary input method.
            st.info("💡 Use the grid above for primary editing. Changes in grid are saved to session memory automatically.")

        except IndexError:
            st.write("No record selected.")
        
        # Update main state if grid changed
        # Note: st.data_editor updates 'edited_df' immediately. 
        # We need to sync edited_df back to st.session_state["data"] respecting the index.
        # For simplicity in this prompt's scope, we assume bulk replacement of matching indices or
        # simple state syncing on specific events.
        # Here we just sync the whole dataset if no filters are active to ensure integrity.
        if len(filtered_df) == len(df):
             # Convert DataFrame back to list of dicts
             # Handle NaN values which Pandas introduces for None
             cleaned_data = edited_df.where(pd.notnull(edited_df), None).to_dict(orient="records")
             st.session_state["data"] = cleaned_data

with tab_valid:
    if st.session_state["validation_issues"]:
        issues_df = pd.DataFrame(st.session_state["validation_issues"])
        
        col_metric1, col_metric2 = st.columns(2)
        error_count = (issues_df["Severity"] == "Error").sum()
        warning_count = (issues_df["Severity"] == "Warning").sum()
        col_metric1.metric("Total Issues", len(issues_df))
        col_metric2.metric("Errors / Warnings", f"{error_count} / {warning_count}")
        st.button("Re-run Validation", on_click=run_validation)
        
        st.dataframe(issues_df, use_container_width=True)
        
        csv_issues = issues_df.to_csv(index=False).encode('utf-8')
        st.download_button("Download Report (CSV)", csv_issues, "validation_report.csv", "text/csv")
    else:
        st.success("No validation issues found! 🎉")

with tab_diff:
    st.markdown("### Compare Original vs Current")
    diff_index = st.number_input("Record Index", 0, len(st.session_state["data"])-1, 0, key="diff_idx")
    
    if len(st.session_state["original_data"]) > diff_index:
        orig = st.session_state["original_data"][diff_index]
        curr = st.session_state["data"][diff_index]
        
        # Calculate diffs manually for display
        diffs_found = False
        for key in ["key_duties_responsibilities", "position_complexity", "organizational_impact"]:
            val_orig = orig.get(key, "")
            val_curr = curr.get(key, "")
            
            if val_orig != val_curr:
                diffs_found = True
                st.markdown(f"#### {key}")
                c1, c2 = st.columns(2)
                c1.text_area("Original", val_orig or "(empty)", height=150, disabled=True, key=f"o_{key}")
                c2.text_area("Current", val_curr, height=150, disabled=True, key=f"c_{key}")
        
        if not diffs_found:
            st.info("No changes detected for this record in key fields.")
    else:
        st.warning("Original data index out of bounds (did you add new records?).")

with tab_export:
    st.markdown("### Download Data")
    st.write(f"{len(st.session_state['data'])} records • {len(st.session_state['changelog'])} changes in log.")
    
    # JSON Export
    json_str = save_json_str(st.session_state["data"])
    st.download_button(
        label="Download Enriched JSON",
        data=json_str,
        file_name="job_descriptions2_enriched.json",
        mime="application/json"
    )
    
    # Changelog Export
    log_str = generate_changelog(st.session_state["changelog"])
    st.download_button(
        label="Download Change Log",
        data=log_str,
        file_name="changelog.json",
        mime="application/json"
    )