# UI Folder

This directory contains all user interface assets for the project, including HTML templates and static files.

## Structure

- `templates/` — Jinja2/Flask HTML templates (e.g., `index.html`).
- (Optional) `static/` — CSS, JS, and image assets for the UI.

## Usage

- Templates are rendered by Flask via `render_template`.
- To add a new page, create a new HTML file in `templates/` and add a corresponding route in `app.py`.

## Guidelines

- Keep templates modular and DRY (use template inheritance).
- Place all static assets in a `static/` subfolder for clarity.
- Document any custom JS or CSS in comments.

## Example

```python
@app.route('/ui')
def serve_ui():
    return render_template('index.html')
``` 