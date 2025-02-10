# GitHub-Style Issue Tracker

A web-based issue tracker that fetches issues from a GitHub repository using the GitHub CLI and API, downloads relevant images, and displays them in a user-friendly interface.

## Features
- Fetches issues from a specified GitHub repository using the GitHub CLI.
- Retrieves comments for each issue via the GitHub API.
- Downloads and displays images embedded in issue descriptions and comments.
- Provides filtering options to view open, closed, or all issues.
- Responsive UI built with Bootstrap 5 and Font Awesome icons.
- Uses Marked.js for rendering Markdown content.

## Installation & Setup

### Prerequisites
Ensure you have the following installed on your system:
- Python (3.x)
- GitHub CLI (`gh`)
- A GitHub personal access token (PAT) with access to issues

### Clone the Repository
```sh
 git clone https://github.com/nazmul-rion/github-issue-exporter.git
 cd github-issue-exporter
```

### Generating a GitHub Personal Access Token (PAT)
1. Go to [GitHub Developer Settings](https://github.com/settings/tokens).
2. Click **Generate new token** (or **Generate new token (classic)** for older versions).
3. Select the necessary scopes:
   - `repo` (for private repositories)
   - `read:org` (if accessing organization repositories)
   - `issues` (to read and fetch issue data)
4. Generate the token and copy it. **Store it securely**, as you won’t be able to see it again.
5. Use this token when prompted by `fetch_issues.py`.

### Setting up GitHub CLI (`gh`)
1. Install GitHub CLI by following the official guide: [GitHub CLI Installation](https://cli.github.com/)
2. Authenticate GitHub CLI by running:
   ```sh
   gh auth login
   ```
   Follow the prompts to authenticate with your GitHub account.
3. Verify authentication:
   ```sh
   gh auth status
   ```
   If authentication is successful, you can proceed with using the script.

### Fetch Issues from GitHub
Run the `fetch_issues.py` script to fetch and save issues in JSON format:
```sh
python fetch_issues.py
```
You'll be prompted to enter:
- GitHub repository owner
- Repository name
- Your GitHub token
- Number of issues to fetch (default: 10)
- Issue state (open, closed, all; default: all)

### Run the Web Interface
Simply open `index.html` in your browser to view the issues in a GitHub-style interface.

## Project Structure
```
📂 your-repo
 ├── 📜 fetch_issues.py      # Python script to fetch issues and download images
 ├── 📜 index.html           # Main web interface
 ├── 📜 issues_with_comments_and_images.json  # Fetched issue data
 ├── 📂 downloaded_images    # Directory for storing downloaded images
 ├── 📜 README.md            # Project documentation
```

## Usage
1. Run `fetch_issues.py` to fetch issues and comments.
2. Open `index.html` in a browser to view the issues.
3. Use the filter dropdown to switch between open, closed, and all issues.

## Dependencies
- Python Modules: `requests`, `json`, `subprocess`, `os`, `time`, `re`
- GitHub CLI: `gh`
- Web Technologies: Bootstrap 5, Font Awesome, Marked.js

If you find this project useful, please ⭐ star it on [GitHub](https://github.com/nazmul-rion/github-issue-tracker)!

## Author
Developed by [Nazmul Islam Rion](https://github.com/nazmul-rion)

