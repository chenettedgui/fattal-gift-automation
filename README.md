# Fattal Gift Automation

Automation framework for Fattal gift voucher purchase flow  
**Python + Selenium + Pytest + Page Object Model (POM)**

## Quick start
```bash
python -m venv .venv
# Windows:
#   .venv\Scripts\activate
# macOS/Linux:
#   source .venv/bin/activate

pip install -r requirements.txt
pytest
```

## Optional environment config
Create a `.env` file in the project root:

```env
BASE_URL=https://projects.whiteweb.co.il/fattal/new/
HEADLESS=false
TIMEOUT=10
```

## Notes
- Locators in the Page Objects are **placeholders** and should be adjusted to the actual DOM.
- Avoid `time.sleep`; use explicit waits provided in `src/core/waits.py`.
