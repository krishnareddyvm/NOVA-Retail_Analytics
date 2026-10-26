import requests
import pandas as pd
import streamlit as st
import plotly.express as px

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="NOVA — Retail Intelligence",
    page_icon="N",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# -----------------------------------------------------------------------------
# NOVA — a monochrome, Vercel-inspired retail intelligence workspace.
# -----------------------------------------------------------------------------
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');

:root {
    --black: #000000;
    --near-black: #030303;
    --surface: #070707;
    --surface-2: #0b0b0b;
    --line: #191919;
    --line-2: #282828;
    --white: #ffffff;
    --moon: #f5f5f5;
    --platinum: #b5b5b5;
    --silver: #8d8d8d;
    --dim: #666666;
}

html, body, [class*="css"] {
    font-family: 'DM Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}
.stApp { background: var(--black); color: var(--moon); }
[data-testid="stHeader"] { background: #000 !important; height: 0 !important; }
[data-testid="stToolbar"] { display: none; }
[data-testid="stSidebar"] { display: none; }
[data-testid="stAppViewContainer"] { background:#000 !important; }
section[data-testid="stMain"] { background:#000 !important; }
button, input, textarea, [role="tab"], [role="radio"] { accent-color:#fff !important; }
*:focus-visible { outline:1px solid #fff !important; outline-offset:2px !important; }
.block-container { max-width: 1320px; padding: 2.8rem 2rem 4rem; }

/* Brand */
.brand-row {
    display:flex; align-items:center; justify-content:space-between;
    padding: 12px 0 22px; border-bottom:1px solid var(--line); min-height:72px;
}
.brand-lockup { display:flex; align-items:center; gap:12px; }
.brand-mark {
    position:relative; width:34px; height:34px; border:1px solid #555;
    border-radius:10px; display:flex; align-items:center; justify-content:center;
    background:#050505; overflow:hidden; box-shadow:0 0 30px rgba(255,255,255,.04);
}
.brand-mark:before {
    content:""; position:absolute; inset:-12px; border-radius:50%;
    border:1px solid #777; opacity:.5; animation:orbit 4s linear infinite;
}
.brand-mark:after {
    content:""; width:8px; height:8px; border-radius:50%; background:#fff;
    box-shadow:0 0 18px rgba(255,255,255,.75); animation:pulse 2s ease-in-out infinite;
}
.brand-name { font-family:'Space Grotesk',sans-serif; font-size:15px; font-weight:700; letter-spacing:-.03em; color:#fff; }
.brand-sub { font-size:11px; color:#666; margin-top:2px; }
.status-pill { border:1px solid var(--line-2); padding:6px 10px; border-radius:999px; color:var(--platinum); font-size:11px; }
.status-dot { display:inline-block; width:6px; height:6px; border-radius:50%; background:#fff; margin-right:7px; box-shadow:0 0 8px rgba(255,255,255,.55); }

@keyframes orbit { to { transform:rotate(360deg); } }
@keyframes pulse { 0%,100% { transform:scale(.75); opacity:.65; } 50% { transform:scale(1.2); opacity:1; } }

/* Navigation */
.nav-wrap { margin:18px 0 30px; }
.nav-wrap [data-testid="stRadio"] > div { background:#050505; border:1px solid var(--line); border-radius:11px; padding:4px; }
.nav-wrap [data-testid="stRadio"] [role="radiogroup"] { gap:3px; }
.nav-wrap [data-testid="stRadio"] label { color:#777 !important; border-radius:8px; padding:8px 16px !important; margin:0 !important; }
.nav-wrap [data-testid="stRadio"] label:has(input:checked) { background:#fff !important; color:#000 !important; }
.nav-wrap [data-testid="stRadio"] label:has(input:checked) p { color:#000 !important; }
.nav-wrap [data-testid="stRadio"] input { display:none; }

/* Hero */
.hero { padding:30px 0 34px; max-width:900px; }
.eyebrow { color:#999; font-size:10px; text-transform:uppercase; letter-spacing:.18em; font-weight:700; }
.hero h1 { font-family:'Space Grotesk',sans-serif; font-size:clamp(42px,6vw,78px); line-height:.98; letter-spacing:-.075em; color:#fff; margin:10px 0 18px; font-weight:600; }
.hero p { color:#8d8d8d; max-width:720px; font-size:15px; line-height:1.75; margin:0; }

/* Cards */
.card { background:linear-gradient(180deg,#070707,#030303); border:1px solid var(--line); border-radius:14px; padding:22px; min-height:132px; }
.card:hover { border-color:#333; }
.card h3 { color:#fff; font-family:'Space Grotesk',sans-serif; font-size:17px; margin:10px 0 7px; letter-spacing:-.025em; }
.muted { color:#777; font-size:13px; line-height:1.6; }
.section-title { font-family:'Space Grotesk',sans-serif; color:#fff; font-size:25px; font-weight:600; letter-spacing:-.045em; margin:30px 0 7px; }
.section-copy { color:#777; font-size:13px; margin-bottom:18px; }

/* Inputs */
[data-testid="stTextInput"] input, [data-testid="stChatInput"] textarea,
div[data-baseweb="select"] > div {
    background:#030303 !important; color:#fff !important; border:1px solid #222 !important;
    border-radius:9px !important; min-height:44px;
}
[data-testid="stTextInput"] input::placeholder, [data-testid="stChatInput"] textarea::placeholder { color:#555 !important; }
[data-testid="stTextInput"] input:focus, [data-testid="stChatInput"] textarea:focus { border-color:#666 !important; box-shadow:0 0 0 1px #444 !important; }
[data-baseweb="select"] span { color:#eee !important; }

/* Buttons */
.stButton > button {
    min-height:42px; background:#060606; color:#ddd; border:1px solid #222;
    border-radius:9px; font-weight:500; transition:all .15s ease;
}
.stButton > button:hover { background:#111; color:#fff; border-color:#444; }
button[kind="primary"] { background:#fff !important; color:#000 !important; border-color:#fff !important; font-weight:600 !important; }
button[kind="primary"]:hover { background:#e7e7e7 !important; border-color:#e7e7e7 !important; }
/* Force Streamlit selection/focus states into the monochrome system. */
[data-baseweb="select"] [aria-selected="true"],
[data-baseweb="menu"] [aria-selected="true"],
[data-baseweb="popover"] [aria-selected="true"] { background:#191919 !important; color:#fff !important; }
[data-testid="stRadio"] label:hover { background:#111 !important; color:#fff !important; }

/* Metrics/table */
[data-testid="stMetric"] { background:#050505; border:1px solid var(--line); border-radius:12px; padding:16px; }
[data-testid="stMetricLabel"] { color:#888 !important; }
[data-testid="stMetricValue"] { color:#fff !important; font-family:'Space Grotesk',sans-serif; }
[data-testid="stDataFrame"] { border:1px solid var(--line); border-radius:12px; overflow:hidden; }
[data-testid="stDataFrame"] * { --primary-color:#fff !important; }

/* Expanders and alerts */
details { background:#050505 !important; border:1px solid #1b1b1b !important; border-radius:10px !important; }
.stAlert { background:#050505 !important; border:1px solid #262626 !important; color:#ddd !important; }
hr { border-color:#161616 !important; }

/* Strict monochrome Streamlit theme overrides */
/* Strict monochrome Streamlit theme overrides */
:root {
    --primary-color: #ffffff !important;
    --secondary-background-color: #080808 !important;
    --background-color: #000000 !important;
    --text-color: #f5f5f5 !important;
}

[data-testid="stAppViewContainer"],
[data-testid="stMain"],
[data-testid="stVerticalBlockBorderWrapper"] {
    color: #f5f5f5 !important;
}

/* Neutral dropdowns */
[data-baseweb="select"] [data-baseweb="popover"] {
    background: #080808 !important;
}

[data-baseweb="menu"] {
    background: #080808 !important;
    border: 1px solid #242424 !important;
}

[data-baseweb="menu"] li:hover,
[data-baseweb="menu"] li[aria-selected="true"] {
    background: #191919 !important;
    color: #ffffff !important;
}

/* MONOCHROME RADIO BUTTONS
   Removes Streamlit's red selected state. */
[data-testid="stRadio"] [role="radio"] {
    accent-color: #ffffff !important;
    background: transparent !important;
    border-color: #666666 !important;
}

[data-testid="stRadio"] [role="radio"][aria-checked="true"] {
    background: #ffffff !important;
    border-color: #ffffff !important;
}

[data-testid="stRadio"] [role="radio"][aria-checked="true"]::after {
    background: #000000 !important;
    border-color: #000000 !important;
}

[data-testid="stRadio"] [role="radio"]:hover {
    border-color: #ffffff !important;
}

/* Catch BaseWeb's actual radio indicator */
[data-testid="stRadio"] [data-baseweb="radio"] > div:first-child {
    border-color: #666666 !important;
    background: transparent !important;
}

[data-testid="stRadio"] [data-baseweb="radio"][aria-checked="true"] > div:first-child,
[data-testid="stRadio"] [data-baseweb="radio"] input:checked + div {
    border-color: #ffffff !important;
    background: #ffffff !important;
}

/* Toasts */
[data-testid="stToast"] {
    background: #0a0a0a !important;
    color: #ffffff !important;
    border: 1px solid #333333 !important;
}

[data-testid="stToast"] * {
    color: #ffffff !important;
}

/* Alerts */
.stAlert {
    background: #080808 !important;
    border: 1px solid #292929 !important;
    color: #dddddd !important;
}

/* Dataframe outer container */
[data-testid="stDataFrame"] {
    border: 1px solid #242424 !important;
    border-radius: 12px !important;
    overflow: hidden !important;
    background: #080808 !important;
}

/* Keep Streamlit's dataframe accent neutral */
[data-testid="stDataFrame"] * {
    --primary-color: #ffffff !important;
}

/* Remove blue focus/selection appearance */
[data-testid="stDataFrame"] *:focus {
    outline-color: #ffffff !important;
}

/* Plotly container — keep the actual graph colors untouched */
.js-plotly-plot {
    border: 1px solid #181818;
    border-radius: 12px;
    overflow: hidden;
}

/* Plotly */
.js-plotly-plot { border:1px solid #181818; border-radius:12px; overflow:hidden; }

/* Topic cards */
.topic-card { background:#050505; border:1px solid #181818; border-radius:12px; padding:16px; margin-bottom:10px; }
.topic-card .topic-title { color:#eee; font-size:13px; font-weight:600; margin-bottom:5px; }
.topic-card .topic-copy { color:#666; font-size:12px; line-height:1.5; }

/* Floating assistant */
.st-key-assistant_popover { position:fixed; right:28px; bottom:24px; z-index:999999; }
.st-key-assistant_popover button {
    width:58px !important; height:58px !important; min-height:58px !important;
    border-radius:50% !important; padding:0 !important; background:#fff !important;
    color:#000 !important; border:1px solid #fff !important; font-family:'Space Grotesk',sans-serif;
    font-size:16px !important; font-weight:700 !important; box-shadow:0 10px 35px rgba(0,0,0,.55), 0 0 0 1px #333;
}
.st-key-assistant_popover button:hover { transform:translateY(-2px); background:#e8e8e8 !important; }

/* Dialog */
[data-testid="stDialog"] > div { background:#050505 !important; border:1px solid #282828 !important; border-radius:16px !important; }
[data-testid="stDialog"] [data-testid="stMarkdownContainer"] h3 { font-family:'Space Grotesk',sans-serif; }

.footer { color:#444; font-size:11px; padding-top:20px; }
</style>
""",
    unsafe_allow_html=True,
)

# ---------- Session state ----------
def init_state():
    defaults = {
        "page": "Home",
        "question": "",
        "pending_question": None,
        "last_result": None,
        "chat_messages": [],
        "assistant_open": False,
        "chart_type": "Bar",
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


init_state()

# ---------- API helpers ----------
def api_health():
    try:
        r = requests.get(f"{API_URL}/health", timeout=2)
        return r.ok
    except requests.RequestException:
        return False


api_online = api_health()


def ui_message(text, kind="info"):
    """Monochrome feedback; avoids Streamlit's red/yellow alert styling."""
    labels = {"success": "Done", "error": "Error", "warning": "Notice", "info": "Info"}
    label = labels.get(kind, "Info")
    st.markdown(
        f'<div class="card" style="min-height:0;padding:12px 15px;margin:10px 0;">'
        f'<span class="eyebrow">{label}</span><div class="muted" style="margin-top:4px;color:#b5b5b5;">{text}</div></div>',
        unsafe_allow_html=True,
    )


def run_query(question, show_feedback=True):
    question = (question or "").strip()
    if not question:
        ui_message("Enter a business question first.", "warning")
        return None
    if not api_online:
        ui_message("FastAPI is not running. Start the backend first.", "error")
        return None
    try:
        r = requests.post(f"{API_URL}/ask", json={"question": question}, timeout=60)
        if not r.ok:
            try:
                detail = r.json().get("detail", r.text)
            except ValueError:
                detail = r.text
            ui_message(f"Request failed: {detail}", "error")
            return None
        data = r.json()
        st.session_state.last_result = data
        if show_feedback:
            ui_message("Query executed successfully.", "success")
        return data
    except requests.RequestException as exc:
        ui_message(f"Could not reach the API: {exc}", "error")
        return None


def open_query(question):
    """Send a topic/assistant query straight to the data view."""
    result = run_query(question, show_feedback=False)
    if result:
        st.session_state.question = question
        st.session_state.page = "Explore"
        st.toast("Opened in Explore")
        st.rerun()


def render_visualizer(df, key_prefix="main"):
    numeric_columns = df.select_dtypes(include="number").columns.tolist()
    label_columns = [c for c in df.columns if c not in numeric_columns]
    if not numeric_columns or not label_columns:
        return

    st.markdown('<div class="section-title">Visualization</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-copy">Change the presentation of the current result without rerunning the query.</div>', unsafe_allow_html=True)

    # Most results contain exactly one sensible label and one sensible measure.
    # Only show selectors when there is genuinely a choice.
    if len(label_columns) == 1 and len(numeric_columns) == 1:
        label, value = label_columns[0], numeric_columns[0]
        chart_type = st.radio(
            "Chart type",
            ["Bar", "Line", "Pie"],
            horizontal=True,
            key=f"{key_prefix}_chart_type",
        )
    else:
        c1, c2 = st.columns(2)
        with c1:
            label = st.selectbox("Category", label_columns, key=f"{key_prefix}_label")
        with c2:
            value = st.selectbox("Measure", numeric_columns, key=f"{key_prefix}_value")
        chart_type = st.radio(
            "Chart type",
            ["Bar", "Line", "Pie"],
            horizontal=True,
            key=f"{key_prefix}_chart_type",
        )

    chart_df = df[[label, value]].dropna().copy()
    if chart_df.empty:
        ui_message("There is no chartable data in this result.", "info")
        return
    chart_df[label] = chart_df[label].astype(str)

    if chart_type == "Bar":
        fig = px.bar(chart_df, x=label, y=value, template="plotly_dark", text_auto=True, color_discrete_sequence=["#f5f5f5"])
    elif chart_type == "Line":
        fig = px.line(chart_df, x=label, y=value, template="plotly_dark", markers=True, color_discrete_sequence=["#f5f5f5"])
    else:
        fig = px.pie(chart_df, names=label, values=value, template="plotly_dark", hole=0.48, color_discrete_sequence=["#ffffff", "#d8d8d8", "#b5b5b5", "#8d8d8d", "#666666"])

    fig.update_layout(
        paper_bgcolor="#000000",
        plot_bgcolor="#000000",
        font=dict(color="#eeeeee", family="DM Sans"),
        margin=dict(l=25, r=25, t=50, b=25),
        title=f"{value.replace('_', ' ').title()} by {label.replace('_', ' ').title()}",
        title_font=dict(color="#ffffff", size=17),
        legend=dict(bgcolor="#000000", font=dict(color="#d4d4d4")),
        hoverlabel=dict(bgcolor="#111111", font=dict(color="#ffffff")),
    )
    fig.update_xaxes(gridcolor="#171717", zerolinecolor="#222222", color="#999999")
    fig.update_yaxes(gridcolor="#171717", zerolinecolor="#222222", color="#999999")
    # The key is deliberately unique per rendered visualizer.
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": True}, key=f"{key_prefix}_plotly")


def render_result(data, show_sql=True):
    if not data:
        return
    result = data.get("result", {})
    rows = result.get("rows", [])
    columns = result.get("columns", [])
    if not rows:
        ui_message("The query returned no rows.", "info")
        return

    df = pd.DataFrame(rows, columns=columns or None)
    numeric = df.select_dtypes(include="number").columns.tolist()
    if len(df) == 1 and numeric:
        metric_cols = st.columns(min(3, len(numeric)))
        for i, col in enumerate(numeric[:3]):
            val = df[col].iloc[0]
            metric_cols[i].metric(col.replace("_", " ").title(), f"{val:,.2f}" if pd.notna(val) else "N/A")

    st.markdown('<div class="section-title">Result</div>', unsafe_allow_html=True)
    st.dataframe(df, use_container_width=True, hide_index=True)

    if len(df) > 1:
        render_visualizer(df, key_prefix="explore")

    insight = data.get("insight")
    if insight:
        st.markdown('<div class="section-title">Insight</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="card"><p class="muted">{insight}</p></div>', unsafe_allow_html=True)

    if show_sql:
        with st.expander("View generated SQL"):
            st.code(data.get("sql", ""), language="sql")


# ---------- Assistant ----------
CONCEPT_ANSWERS = {
    "average order value": "Average Order Value (AOV) is total revenue divided by the number of orders. It estimates the revenue generated by a typical order.",
    "revenue and profit": "Revenue is the money generated by sales. Profit is what remains after relevant costs are subtracted. This dataset focuses on sales and revenue rather than a complete accounting profit model.",
    "line chart": "Use a line chart when the horizontal dimension has an order, especially time. It makes trends and changes easier to see.",
    "bar chart": "Use a bar chart when the goal is to compare discrete categories such as products, cities, regions, or payment methods.",
    "pie chart": "Use a pie chart when you want to show how a small number of categories contribute to a whole.",
    "sql": "SQL is the language used to retrieve and aggregate the SQLite data. NOVA generates read-only SELECT queries from natural-language business questions.",
    "database": "NOVA uses a SQLite database containing customers, products, employees, orders, and payments.",
}

TOPIC_PROMPTS = [
    ("Revenue overview", "What is the total revenue?"),
    ("Monthly trend", "Show monthly revenue"),
    ("Top products", "Show top 5 products"),
    ("Category mix", "Show sales by category"),
    ("Regional sales", "Show sales by region"),
    ("Payment mix", "Show sales by payment method"),
    ("Top cities", "Show top 5 cities by revenue"),
    ("Top employees", "Show top 5 employees by revenue"),
    ("Top categories", "Show top 5 categories by revenue"),
    ("Sales by state", "Show sales by state"),
    ("Monthly orders", "Show monthly orders"),
    ("Order value", "What is the average order value?"),
    ("Order volume", "What is the total number of orders?"),
    ("Discount", "What is the average discount?"),
]


def assistant_reply(message):
    lowered = message.lower().strip()
    if not api_online:
        return {"reply": "The analytics backend is offline. Start FastAPI and try again.", "result": None}

    # Let the backend decide whether this is a database question.
    try:
        response = requests.post(f"{API_URL}/chat", json={"message": message}, timeout=60)
        if response.ok:
            payload = response.json()
            if payload.get("data_query") and payload.get("result"):
                return {
                    "reply": "I ran that question against the retail database. The result is now open in Explore.",
                    "result": {
                        "question": message,
                        "sql": payload.get("sql", ""),
                        "result": payload.get("result", {}),
                    },
                }
            reply = payload.get("reply")
            if reply:
                return {"reply": reply, "result": None}
    except requests.RequestException:
        pass

    for key, reply in CONCEPT_ANSWERS.items():
        if key in lowered:
            return {"reply": reply, "result": None}

    return {
        "reply": "I can answer questions about revenue, products, customers, orders, SQL, the database, and chart selection. You can also choose a ready-made business question below and I will open its result directly.",
        "result": None,
    }


def render_assistant_popover():
    """Compact assistant opened from the floating bottom-right control."""
    with st.popover("N.", key="assistant_popover"):
        st.markdown("### NOVA Assistant")
        st.caption("Ask a question, or choose a prompt to open its live result in Explore.")

        for message in st.session_state.chat_messages[-6:]:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        st.markdown("**Quick questions**")
        cols = st.columns(2)
        for i, (label, query) in enumerate(TOPIC_PROMPTS):
            with cols[i % 2]:
                if st.button(label, use_container_width=True, key=f"assistant_topic_{i}"):
                    result = run_query(query, show_feedback=False)
                    if result:
                        st.session_state.last_result = result
                        st.session_state.question = query
                        st.session_state.page = "Explore"
                        st.session_state.chat_messages.append({"role": "assistant", "content": f"Opened the result for **{query}** in Explore."})
                        st.toast("Opened in Explore")
                        st.rerun()

        prompt = st.text_input(
            "Ask NOVA",
            placeholder="e.g. What is the average order value?",
            key="assistant_prompt",
        )
        if st.button("Ask", type="primary", use_container_width=True, key="assistant_send"):
            if prompt.strip():
                st.session_state.chat_messages.append({"role": "user", "content": prompt.strip()})
                answer = assistant_reply(prompt.strip())
                st.session_state.chat_messages.append({"role": "assistant", "content": answer["reply"]})
                if answer["result"]:
                    st.session_state.last_result = answer["result"]
                    st.session_state.question = prompt.strip()
                    st.session_state.page = "Explore"
                st.rerun()


# ---------- Header ----------
status_text = "Backend online" if api_online else "Backend offline"
st.markdown(
    """
<div class="brand-row">
  <div class="brand-lockup">
    <div class="brand-mark"></div>
    <div>
      <div class="brand-name">NOVA</div>
      <div class="brand-sub">Retail intelligence workspace</div>
    </div>
  </div>
  <div class="status-pill"><span class="status-dot"></span>{status_text}</div>
</div>
""".format(status_text=status_text),
    unsafe_allow_html=True,
)

# Navigation is intentionally compact rather than a permanent sidebar.
nav_options = ["Home", "Explore", "Topics & Guide"]
if st.session_state.page not in nav_options:
    st.session_state.page = "Home"

st.markdown('<div class="nav-wrap">', unsafe_allow_html=True)
st.session_state.page = st.radio(
    "Workspace",
    nav_options,
    index=nav_options.index(st.session_state.page),
    horizontal=True,
    label_visibility="collapsed",
    key="main_navigation",
)
st.markdown('</div>', unsafe_allow_html=True)

# ---------- Home ----------
if st.session_state.page == "Home":
    st.markdown(
        """
<div class="hero">
  <div class="eyebrow">Natural language business intelligence</div>
  <h1>Ask your data.</h1>
  <p>NOVA turns plain-English business questions into safe database queries, gives you the result, and lets you reshape the answer into the visualization that makes the most sense.</p>
</div>
""",
        unsafe_allow_html=True,
    )

    status_cols = st.columns(3)
    status_cols[0].metric("API", "Online" if api_online else "Offline")
    status_cols[1].metric("Database", "SQLite")
    status_cols[2].metric("Access", "Read-only")

    st.markdown('<div class="section-title">Workspace</div>', unsafe_allow_html=True)
    a, b, c = st.columns(3)
    with a:
        st.markdown('<div class="card"><div class="eyebrow">01 · Explore</div><h3>Ask in plain English</h3><p class="muted">Write a business question and NOVA converts it into a safe, read-only query.</p></div>', unsafe_allow_html=True)
    with b:
        st.markdown('<div class="card"><div class="eyebrow">02 · Understand</div><h3>Read the result</h3><p class="muted">Inspect the returned data, generated SQL, and the key insight from your question.</p></div>', unsafe_allow_html=True)
    with c:
        st.markdown('<div class="card"><div class="eyebrow">03 · Present</div><h3>Shape the story</h3><p class="muted">Switch the same result between bar, line, and pie views instantly.</p></div>', unsafe_allow_html=True)

    st.markdown('<div class="section-title">Start with a question</div>', unsafe_allow_html=True)
    cols = st.columns(3)
    for i, (label, query) in enumerate(TOPIC_PROMPTS[:6]):
        with cols[i % 3]:
            if st.button(label, use_container_width=True, key=f"home_prompt_{i}"):
                open_query(query)

# ---------- Explore: query + visualization in ONE workspace ----------
elif st.session_state.page == "Explore":
    st.markdown('<div class="section-title">Explore</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-copy">One workspace for the question, result, insight, SQL, and interactive visualization. Nothing is duplicated across separate tabs.</div>', unsafe_allow_html=True)

    question = st.text_input(
        "Business question",
        value=st.session_state.question,
        placeholder="e.g. Show monthly revenue",
        key="explore_question",
    )
    c1, c2 = st.columns([1, 5])
    with c1:
        if st.button("Run query", type="primary", use_container_width=True, key="run_explore"):
            result = run_query(question)
            if result:
                st.session_state.question = question
                st.rerun()
    with c2:
        st.caption("Examples: total revenue · top 5 products · sales by region · monthly revenue")

    if st.session_state.last_result:
        render_result(st.session_state.last_result)
    else:
        st.markdown('<div class="card"><div class="eyebrow">Waiting for a question</div><h3>Your analysis will appear here</h3><p class="muted">Run a question from this page or use the floating NOVA Assistant.</p></div>', unsafe_allow_html=True)

# ---------- Topics ----------
else:
    st.markdown('<div class="section-title">Topics & Guide</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-copy">These are curated prompts for the retail dataset. Choose one to open its live result in Explore, or ask NOVA about the concept.</div>', unsafe_allow_html=True)

    groups = {
        "Revenue & Sales": [TOPIC_PROMPTS[i] for i in [0, 1, 3, 4, 5, 8, 10]],
        "Products & Orders": [
            TOPIC_PROMPTS[2], TOPIC_PROMPTS[7], TOPIC_PROMPTS[8],
            ("Order quantity", "Show order quantity by product"),
            TOPIC_PROMPTS[11], TOPIC_PROMPTS[12],
        ],
        "Customers & Geography": [
            TOPIC_PROMPTS[6], TOPIC_PROMPTS[9],
            ("Highest-revenue city", "Which city has the highest revenue?"),
            ("Customers in Pune", "Show customers from Pune"),
        ],
        "Analytics concepts": [
            ("Average order value", "What is an average order value?"),
            ("Revenue vs profit", "What is the difference between revenue and profit?"),
            ("Line chart", "When should I use a line chart?"),
            ("Bar chart", "When should I use a bar chart?"),
            ("Pie chart", "When is a pie chart useful?"),
            ("SQL", "What is SQL and why is it used here?"),
        ],
    }

    for group, prompts in groups.items():
        st.markdown(f"### {group}")
        cols = st.columns(3)
        for i, (label, query) in enumerate(prompts):
            with cols[i % 3]:
                st.markdown(f'<div class="topic-card"><div class="topic-title">{label}</div><div class="topic-copy">{query}</div></div>', unsafe_allow_html=True)
                if group == "Analytics concepts":
                    if st.button("Ask NOVA", key=f"concept_{i}_{group}", use_container_width=True):
                        st.session_state.chat_messages.append({"role": "user", "content": query})
                        answer = assistant_reply(query)
                        st.session_state.chat_messages.append({"role": "assistant", "content": answer["reply"]})
                        st.session_state.page = "Topics & Guide"
                        st.toast("NOVA answered your question")
                        st.rerun()
                else:
                    if st.button("Open result", key=f"topic_{i}_{group}", use_container_width=True):
                        open_query(query)

# ---------- Floating assistant ----------
# One small, monochrome bubble stays available from every page.
st.markdown('<div class="assistant-spacer"></div>', unsafe_allow_html=True)
render_assistant_popover()

st.markdown('<div class="footer">NOVA · FastAPI · SQLite · Streamlit</div>', unsafe_allow_html=True)
