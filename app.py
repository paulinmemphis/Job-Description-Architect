import streamlit as st
import pandas as pd
from datetime import datetime

from core.schema import JobRecord
from core.enhance import bulk_enhance
from core.validate import validate_dataset
from core.io import load_json, save_json_str, generate_changelog, deduplicate_data
from core.constants import CAREER_FAMILIES

# --- CONFIG ---
st.set_page_config(
    page_title="Job Description Architect",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- STATE MANAGEMENT ---
if "data" not in st.session_state:
    st.session_state["data"] = []  # The working list of dicts
if "original_data" not in st.session_state:
    st.session_state["original_data"] = []  # For diffing
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
        st.session_state["original_data"] = [r.copy() for r in raw_data]  # Deep copy for diff
        st.session_state["file_loaded"] = True
        st.session_state["changelog"] = []
        run_validation()
        st.sidebar.success(f"Loaded {len(raw_data)} records.")
    except Exception as e:
        st.sidebar.error(f"Error loading file: {e}")


if uploaded_file:
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
    try:
        records_objs = []
        indices = []

        for idx, r in enumerate(st.session_state["data"]):
            try:
                records_objs.append(JobRecord(**r))
                indices.append(idx)
            except Exception:
                continue

        enhanced_objs, count = bulk_enhance(records_objs)

        new_data = list(st.session_state["data"])
        narrative_fields = [
            "key_duties_responsibilities",
            "position_complexity",
            "organizational_impact",
            "career_progression_path",
        ]

        for rec_index, enhanced_rec in zip(indices, enhanced_objs):
            base = dict(new_data[rec_index])
            enhanced_dict = enhanced_rec.model_dump()

            for field in narrative_fields:
                if field in enhanced_dict and enhanced_dict[field] is not None:
                    base[field] = enhanced_dict[field]

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

        st.session_state["data"] = new_data

        st.session_state["changelog"].append({
            "timestamp": datetime.now().isoformat(),
            "action": "bulk_enhance",
            "records_modified": count,
        })

        st.toast(f"Enhanced {count} records!", icon="✨")
        run_validation()
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


def sync_grid_to_session(edited_df: pd.DataFrame):
    """Persist grid edits back to the main session data, even when filtered."""
    cleaned_df = edited_df.where(pd.notnull(edited_df), None)
    base_data = list(st.session_state["data"])

    for _, row in cleaned_df.iterrows():
        row_dict = row.to_dict()
        orig_index = row_dict.pop("_orig_index", None)

        try:
            orig_index_int = int(orig_index) if orig_index is not None else None
        except (TypeError, ValueError):
            orig_index_int = None

        if orig_index_int is not None and 0 <= orig_index_int < len(base_data):
            base_data[orig_index_int] = {
                **base_data[orig_index_int],
                **row_dict,
            }
        else:
            base_data.append(row_dict)

    st.session_state["data"] = base_data


filtered_df = df.copy()
if not filtered_df.empty:
    if filter_families:
        filtered_df = filtered_df[filtered_df["careerFamily"].isin(filter_families)]
    if filter_depts:
        filtered_df = filtered_df[filtered_df["department"].isin(filter_depts)]
    if search_term:
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
        editable_df = filtered_df.reset_index().rename(columns={"index": "_orig_index"})

        edited_df = st.data_editor(
            editable_df,
            num_rows="dynamic",
            use_container_width=True,
            key="main_editor",
            column_config={
                "_orig_index": st.column_config.NumberColumn(
                    "Row ID", disabled=True, help="Original row reference"
                ),
            },
            hide_index=True,
        )

        sync_grid_to_session(edited_df)

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

        try:
            selected_row = edited_df.iloc[selected_index]
            selected_orig_idx_raw = selected_row.get("_orig_index")
            selected_orig_idx = (
                int(selected_orig_idx_raw) if pd.notnull(selected_orig_idx_raw) else None
            )

            if selected_orig_idx is not None and 0 <= selected_orig_idx < len(st.session_state["data"]):
                record_to_edit = st.session_state["data"][selected_orig_idx]
            else:
                record_to_edit = {k: v for k, v in selected_row.to_dict().items() if k != "_orig_index"}

            input_suffix = selected_orig_idx if selected_orig_idx is not None else f"new_{selected_index}"
            col1, col2 = st.columns(2)
            with col1:
                new_title = st.text_input(
                    "Position Title",
                    record_to_edit.get("positionTitle", ""),
                    key=f"title_{input_suffix}",
                )
                new_dept = st.text_input(
                    "Department",
                    record_to_edit.get("department", ""),
                    key=f"dept_{input_suffix}",
                )
                current_family = record_to_edit.get("careerFamily")
                family_index = CAREER_FAMILIES.index(current_family) if current_family in CAREER_FAMILIES else 0
                new_family = st.selectbox(
                    "Career Family",
                    options=CAREER_FAMILIES,
                    index=family_index,
                    key=f"family_{input_suffix}",
                )
                new_job_level = st.text_input(
                    "Job Level",
                    record_to_edit.get("jobLevel", ""),
                    key=f"job_level_{input_suffix}",
                )

            with col2:
                st.markdown("**Generated Content**")
                new_duties = st.text_area(
                    "Duties",
                    record_to_edit.get("key_duties_responsibilities", ""),
                    height=150,
                    key=f"duties_{input_suffix}",
                )
                new_complex = st.text_area(
                    "Complexity",
                    record_to_edit.get("position_complexity", ""),
                    height=100,
                    key=f"complexity_{input_suffix}",
                )
                new_impact = st.text_area(
                    "Organizational Impact",
                    record_to_edit.get("organizational_impact", ""),
                    height=100,
                    key=f"impact_{input_suffix}",
                )
                new_progression = st.text_area(
                    "Career Progression",
                    record_to_edit.get("career_progression_path", ""),
                    height=100,
                    key=f"progression_{input_suffix}",
                )

            if st.button("Save Detail Edits", key=f"save_detail_{input_suffix}"):
                updated_record = {
                    **{k: v for k, v in record_to_edit.items() if k != "_orig_index"},
                    "positionTitle": new_title,
                    "department": new_dept,
                    "careerFamily": new_family,
                    "jobLevel": new_job_level,
                    "key_duties_responsibilities": new_duties,
                    "position_complexity": new_complex,
                    "organizational_impact": new_impact,
                    "career_progression_path": new_progression,
                }

                data_copy = list(st.session_state["data"])
                if selected_orig_idx is not None and 0 <= selected_orig_idx < len(data_copy):
                    data_copy[selected_orig_idx] = updated_record
                else:
                    data_copy.append(updated_record)

                st.session_state["data"] = data_copy
                st.session_state["changelog"].append({
                    "timestamp": datetime.now().isoformat(),
                    "action": "detail_edit",
                    "record_index": selected_orig_idx,
                })
                run_validation()
                st.toast("Detail changes saved.", icon="💾")
                st.rerun()

        except IndexError:
            st.write("No record selected.")

        st.info("💡 Edits in the grid are saved automatically; use the detail editor for focused updates.")

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

    json_str = save_json_str(st.session_state["data"])
    st.download_button(
        label="Download Enriched JSON",
        data=json_str,
        file_name="job_descriptions2_enriched.json",
        mime="application/json"
    )

    log_str = generate_changelog(st.session_state["changelog"])
    st.download_button(
        label="Download Change Log",
        data=log_str,
        file_name="changelog.json",
        mime="application/json",
    )
