# ⚙️ Setup Guide — Daily Project Automation

Follow these steps once to get the automation running on GitHub.

---

## Step 1 — Create a GitHub repository

1. Go to https://github.com/new
2. Name it: `daily-data-ml-projects`
3. Set it to **Public** (so it appears on your profile)
4. Do **not** initialize with a README (you already have one)
5. Click **Create repository**

---

## Step 2 — Upload this folder to GitHub

On your local machine, run:

```bash
# Navigate to the folder you downloaded
cd daily-projects

# Initialize git and push
git init
git add .
git commit -m "Initial setup — daily project automation"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/daily-data-ml-projects.git
git push -u origin main
```

Replace `YOUR_USERNAME` with your actual GitHub username.

---

## Step 3 — Verify GitHub Actions is enabled

1. Go to your repo on GitHub
2. Click the **Actions** tab
3. You should see **"Daily Project Generator"** listed
4. If prompted, click **"I understand my workflows, go ahead and enable them"**

---

## Step 4 — Test it manually (recommended)

Don't wait until tomorrow — run it now:

1. Go to **Actions** tab
2. Click **"Daily Project Generator"** in the left sidebar
3. Click **"Run workflow"** → **"Run workflow"** button
4. Watch it run — a new project folder should appear in `projects/`

---

## Step 5 — Schedule

The workflow runs automatically every day at:
- **6:00 AM UTC**
- **11:30 AM IST**

You can change the time by editing `.github/workflows/daily-project.yml`:
```yaml
- cron: "0 6 * * *"   # change 6 to your preferred UTC hour
```

---

## Customising projects

To add your own project ideas, edit `scripts/generate_project.py` and add a new entry to the `PROJECTS` list following the same format:

```python
{
    "category": "ML",          # or "Data Analysis", "NLP", "BI"
    "title": "My Project Title",
    "description": "One line description.",
    "skills": ["pandas", "scikit-learn"],
    "code": '''
# your Python code here
''',
},
```

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Workflow not running | Check Actions tab is enabled in repo settings |
| Push permission error | Ensure `permissions: contents: write` is in the YAML |
| Nothing committed | The script may have already run today — check `projects/LOG.md` |
| Import errors | The workflow installs: pandas, numpy, matplotlib, scikit-learn, statsmodels |
