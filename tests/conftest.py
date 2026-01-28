import json
import re
import time
from datetime import datetime
from pathlib import Path

import pytest

from src.core.driver_factory import create_driver


# =========================================================
# Dashboard settings
# =========================================================
DASHBOARD_TITLE = "Fattal QA Automation Dashboard - Fattal- Gift"
LOGO_FILENAME = "logo.svg"  # must exist in PROJECT ROOT


# =========================================================
# Paths / folders
# =========================================================
PROJECT_ROOT = Path(__file__).resolve().parents[1]  # tests/ -> project root
REPORTS_DIR = PROJECT_ROOT / "reports"
RUNS_DIR = REPORTS_DIR / "runs"
ASSETS_DIR = REPORTS_DIR / "assets"


def _safe_filename(name: str) -> str:
    name = name.strip().replace(" ", "_")
    return re.sub(r"[^a-zA-Z0-9_\-\.]", "_", name)


def _now_run_id() -> str:
    return "run_" + datetime.now().strftime("%Y-%m-%d_%H-%M-%S")


def _ensure_assets():
    """
    Copies project-root logo.svg into:
      reports/assets/logo.svg
      reports/assets/favicon.svg
    """
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)

    src_logo = PROJECT_ROOT / LOGO_FILENAME
    dst_logo = ASSETS_DIR / "logo.svg"
    dst_favicon = ASSETS_DIR / "favicon.svg"

    if src_logo.exists():
        dst_logo.write_bytes(src_logo.read_bytes())
        dst_favicon.write_bytes(src_logo.read_bytes())


def _load_all_runs() -> dict:
    run_data = {}
    if not RUNS_DIR.exists():
        return run_data

    for run_folder in sorted(RUNS_DIR.iterdir(), reverse=True):
        if not run_folder.is_dir():
            continue
        data_file = run_folder / "run_data.json"
        if data_file.exists():
            try:
                run_data[run_folder.name] = json.loads(data_file.read_text(encoding="utf-8"))
            except Exception:
                pass
    return run_data


def _format_run_label(run_id: str, tests: list[dict]) -> str:
    try:
        dt = datetime.strptime(run_id.replace("run_", ""), "%Y-%m-%d_%H-%M-%S")
        day_name = dt.strftime("%A")
        ts = dt.strftime("%Y-%m-%d %H:%M:%S")
    except Exception:
        day_name = ""
        ts = run_id

    total = len(tests)
    passed = sum(1 for t in tests if t.get("status") == "PASSED")
    failed = sum(1 for t in tests if t.get("status") == "FAILED")
    desktop = total

    return f"{day_name} {ts} | {total} tests | ✅ {passed} | ❌ {failed} | 💻 {desktop}"


def _build_dashboard_html(run_data: dict, selected_run_id: str, mode: str) -> str:
    """
    mode:
      - "root": for reports/Dashboard.html
      - "per_run": for reports/runs/<run_id>/Dashboard.html
    """
    if mode == "root":
        logo_path = "assets/logo.svg"
        favicon_path = "assets/favicon.svg"
        screenshots_src_prefix = "runs/{runId}/Screenshots/{file}"
    else:
        # per-run dashboard is inside reports/runs/<run_id>/Dashboard.html
        logo_path = "../../assets/logo.svg"
        favicon_path = "../../assets/favicon.svg"
        screenshots_src_prefix = "Screenshots/{file}"

    options_html = []
    for run_id in sorted(run_data.keys(), reverse=True):
        tests = run_data.get(run_id, [])
        label = _format_run_label(run_id, tests)
        selected = "selected" if run_id == selected_run_id else ""
        options_html.append(f'<option value="{run_id}" {selected}>{label}</option>')
    options_html = "\n".join(options_html)

    run_data_json = json.dumps(run_data, ensure_ascii=False)

    return f"""<!DOCTYPE html>
<html lang="he">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <title>{DASHBOARD_TITLE}</title>
  <link rel="icon" type="image/svg+xml" href="{favicon_path}">
  <style>
    body {{
      font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
      background-color: #f9f9f9;
      margin: 20px;
      color: #333;
    }}
    .dashboard-header {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 10px;
      gap: 24px;
    }}
    .dashboard-header h1 {{
      margin: 0;
      font-size: 1.8em;
      display: flex;
      align-items: center;
      white-space: nowrap;
    }}
    .dashboard-header h1::before {{
      content: '🧪';
      margin-right: 10px;
    }}
    .header-logo {{
      height: 60px;
      max-width: 240px;
      object-fit: contain;
      border-radius: 8px;
      background: #fff;
      padding: 6px 12px;
      box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    }}
    @media (max-width: 700px) {{
      .dashboard-header {{
        flex-direction: column;
        align-items: flex-start;
        gap: 8px;
      }}
      .header-logo {{
        margin-left: 0;
        margin-top: 6px;
        height: 44px;
        max-width: 180px;
      }}
    }}

    select {{
      font-size: 14px;
      padding: 5px;
      margin-left: 10px;
    }}

    .test-entry {{
      background: #fff;
      border-radius: 6px;
      padding: 15px;
      margin-bottom: 20px;
      box-shadow: 0 1px 4px rgba(0,0,0,0.1);
      transition: background 0.2s ease;
    }}
    .test-entry:hover {{
      background: #f0f8ff;
    }}

    .meta-line {{
      margin: 6px 0 0 0;
      font-size: 14px;
    }}

    /* 4-step grid */
    .steps-grid {{
      display: grid;
      grid-template-columns: repeat(4, minmax(140px, 1fr));
      gap: 14px;
      margin-top: 12px;
      align-items: start;
    }}
    @media (max-width: 1000px) {{
      .steps-grid {{
        grid-template-columns: repeat(2, minmax(140px, 1fr));
      }}
    }}
    @media (max-width: 520px) {{
      .steps-grid {{
        grid-template-columns: 1fr;
      }}
    }}

    .step-card {{
      display: flex;
      flex-direction: column;
      gap: 6px;
    }}
    .step-title {{
      font-weight: 700;
      font-size: 13px;
      color: #222;
    }}
    .step-card img {{
      width: 100%;
      height: auto;
      max-height: 190px;
      object-fit: contain;
      border-radius: 6px;
      border: 1px solid #ccc;
      background: #fff;
      cursor: pointer;
    }}

    /* Modal */
    .modal {{
      display: none;
      position: fixed;
      z-index: 999;
      left: 0; top: 0; width: 100%; height: 100%;
      background-color: rgba(0,0,0,0.85);
    }}
    .modal-content {{
      margin: 5% auto;
      display: block;
      max-width: 92vw;
      max-height: 84vh;
    }}
    .close {{
      position: absolute;
      top: 15px;
      right: 35px;
      color: #fff;
      font-size: 40px;
      font-weight: bold;
      cursor: pointer;
    }}

    /* Back-to-top button */
    #backToTop {{
      position: fixed;
      bottom: 18px;
      right: 18px;
      width: 46px;
      height: 46px;
      border-radius: 999px;
      border: none;
      background: #111827;
      color: white;
      font-size: 22px;
      cursor: pointer;
      display: none;
      box-shadow: 0 8px 20px rgba(0,0,0,0.22);
    }}
    #backToTop:hover {{
      background: #0b1220;
    }}
  </style>

  <script>
    const runData = {run_data_json};
    const screenshotsPrefix = `{screenshots_src_prefix}`;

    function openModal(src) {{
      const modal = document.getElementById("screenshotModal");
      const modalImg = document.getElementById("modalImage");
      modal.style.display = "block";
      modalImg.src = src;
    }}

    function closeModal() {{
      document.getElementById("screenshotModal").style.display = "none";
    }}

    function imgSrc(runId, file) {{
      return screenshotsPrefix
        .replace("{{runId}}", runId)
        .replace("{{file}}", file);
    }}

    function populateRun(runId) {{
      const container = document.getElementById("results");
      container.innerHTML = "";

      const showPassed = document.getElementById("filterPassed").checked;
      const showFailed = document.getElementById("filterFailed").checked;

      const data = runData[runId] || [];
      data.forEach(test => {{
        if ((test.status === "PASSED" && !showPassed) || (test.status === "FAILED" && !showFailed)) return;

        const div = document.createElement("div");
        div.classList.add("test-entry");

        const color = test.status === "PASSED" ? "green" : "red";

        const steps = Array.isArray(test.steps) ? test.steps.slice(0, 4) : [];
        const hasSteps = steps.length > 0;

        let gridHtml = "";

        if (hasSteps) {{
          const cards = steps.map(s => {{
            const src = imgSrc(runId, s.file);
            return `
              <div class="step-card">
                <div class="step-title">${{s.label}}</div>
                <img src="${{src}}" onclick="openModal(this.src)" />
              </div>
            `;
          }}).join("");

          gridHtml = `<div class="steps-grid">${{cards}}</div>`;
        }} else {{
          if (test.final_screenshot) {{
            const src = imgSrc(runId, test.final_screenshot);
            gridHtml = `
              <div class="steps-grid" style="grid-template-columns: minmax(200px, 340px);">
                <div class="step-card">
                  <div class="step-title">final_screenshot</div>
                  <img src="${{src}}" onclick="openModal(this.src)" />
                </div>
              </div>
            `;
          }}
        }}

        div.innerHTML = `
          <h3>${{test.name}} — <span style="color:${{color}}">${{test.status}}</span></h3>
          <p class="meta-line"><strong>Timestamp:</strong> ${{test.timestamp}} | <strong>Duration:</strong> ${{test.duration}}</p>
          ${{gridHtml}}
          <hr>
        `;

        container.appendChild(div);
      }});
    }}

    window.addEventListener("scroll", () => {{
      const btn = document.getElementById("backToTop");
      btn.style.display = (window.scrollY > 450) ? "block" : "none";
    }});

    function backToTop() {{
      window.scrollTo({{ top: 0, behavior: "smooth" }});
    }}
  </script>
</head>

<body onload="populateRun(document.getElementById('runSelect').value)">
  <div class="dashboard-header">
    <h1>{DASHBOARD_TITLE}</h1>
    <img src="{logo_path}" alt="Fattal Logo" class="header-logo" />
  </div>

  <label>Choose Run:
    <select id="runSelect" onchange="populateRun(this.value)">
      {options_html}
    </select>
  </label>

  <div style="margin-top: 10px;">
    <label><input type="checkbox" id="filterPassed" checked onchange="populateRun(document.getElementById('runSelect').value)"> Show Passed</label>
    <label><input type="checkbox" id="filterFailed" checked onchange="populateRun(document.getElementById('runSelect').value)"> Show Failed</label>
  </div>

  <div id="results" style="margin-top: 20px;"></div>

  <button id="backToTop" onclick="backToTop()" title="Back to top">↑</button>

  <div id="screenshotModal" class="modal" onclick="closeModal()">
    <span class="close">&times;</span>
    <img class="modal-content" id="modalImage">
  </div>
</body>
</html>
"""


# =========================================================
# Pytest run state (per run)
# =========================================================
_CURRENT_RUN_ID = None
_CURRENT_RUN_DIR = None
_CURRENT_SCREENSHOTS_DIR = None
_TEST_RESULTS = []


@pytest.fixture
def driver():
    drv = create_driver()
    yield drv
    drv.quit()


@pytest.fixture
def capture_step(request, driver):
    """
    Optional: capture up to 4 step screenshots per test.
    If not used -> dashboard shows only final screenshot.
    """
    def _capture(label: str):
        label_clean = (label or "step").strip()
        safe_label = _safe_filename(label_clean)
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f"{_safe_filename(request.node.nodeid)}__{safe_label}_{ts}.png"
        path = _CURRENT_SCREENSHOTS_DIR / file_name
        driver.save_screenshot(str(path))

        if not hasattr(request.node, "_step_screenshots"):
            request.node._step_screenshots = []

        if len(request.node._step_screenshots) < 4:
            request.node._step_screenshots.append({"label": label_clean, "file": file_name})

    return _capture


def pytest_sessionstart(session):
    global _CURRENT_RUN_ID, _CURRENT_RUN_DIR, _CURRENT_SCREENSHOTS_DIR, _TEST_RESULTS

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    RUNS_DIR.mkdir(parents=True, exist_ok=True)

    _ensure_assets()

    _CURRENT_RUN_ID = _now_run_id()
    _CURRENT_RUN_DIR = RUNS_DIR / _CURRENT_RUN_ID
    _CURRENT_SCREENSHOTS_DIR = _CURRENT_RUN_DIR / "Screenshots"

    _CURRENT_SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)
    _TEST_RESULTS = []


def pytest_runtest_setup(item):
    item._start_time = time.perf_counter()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()

    if rep.when != "call":
        return

    drv = item.funcargs.get("driver", None)

    start = getattr(item, "_start_time", None)
    dur_sec = (time.perf_counter() - start) if start else 0.0

    status = "PASSED" if rep.passed else "FAILED"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    duration = f"{dur_sec:.2f}s"

    screenshot_file = ""
    if drv is not None:
        safe = _safe_filename(item.nodeid)
        screenshot_file = f"{safe}_{status}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        screenshot_path = _CURRENT_SCREENSHOTS_DIR / screenshot_file
        try:
            drv.save_screenshot(str(screenshot_path))
        except Exception:
            screenshot_file = ""

    steps = getattr(item, "_step_screenshots", [])
    if not isinstance(steps, list):
        steps = []

    _TEST_RESULTS.append({
        "name": item.name,
        "status": status,
        "timestamp": timestamp,
        "duration": duration,
        "final_screenshot": screenshot_file,
        "steps": steps[:4],
    })


def pytest_sessionfinish(session, exitstatus):
    _ensure_assets()

    run_data_file = _CURRENT_RUN_DIR / "run_data.json"
    run_data_file.write_text(json.dumps(_TEST_RESULTS, ensure_ascii=False, indent=2), encoding="utf-8")

    all_runs = _load_all_runs()
    all_runs[_CURRENT_RUN_ID] = _TEST_RESULTS

    # Per-run dashboard (paths adjusted)
    per_run_html = _build_dashboard_html({_CURRENT_RUN_ID: _TEST_RESULTS}, selected_run_id=_CURRENT_RUN_ID, mode="per_run")
    (_CURRENT_RUN_DIR / "Dashboard.html").write_text(per_run_html, encoding="utf-8")

    # Main dashboard (always named Dashboard.html)
    main_html = _build_dashboard_html(all_runs, selected_run_id=_CURRENT_RUN_ID, mode="root")
    (REPORTS_DIR / "Dashboard.html").write_text(main_html, encoding="utf-8")
