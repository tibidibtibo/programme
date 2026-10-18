import re
import os

INDEX_FILE = "programme/00-index.md"
DOMAINS_DIR = "programme/domaines"

def verify():
    # very simple check to ensure no file is missing the basic structures
    with open(INDEX_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    assert "≈ 81 Md€" in content, "Socle missing 81"
    assert "≈ 40 Md€" in content, "Vague 2 missing 40"

    files = [f for f in os.listdir(DOMAINS_DIR) if f.endswith('.md')]
    for file in files:
        with open(os.path.join(DOMAINS_DIR, file), 'r', encoding='utf-8') as f:
            fc = f.read()
            if not "Chiffrage" in fc and not file in ["00-index.md", "programme-v1.md"]:
                print(f"Warning: {file} might be missing Chiffrage section.")

    print("Verification passed (basic struct check).")

if __name__ == "__main__":
    verify()
