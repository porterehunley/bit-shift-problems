import os
import re
from pathlib import Path
import shutil

TEMPLATE_PATH = Path(__file__).parent.parent / "templates" / "problem_template.md"

def slugify(title):
  """Convert title to a slug suitable for a file name."""
  slug = title.lower()
  slug = re.sub(r'[^\w\s-]', '', slug)
  slug = re.sub(r'[\s]+', '-', slug)
  return slug

def generate_markdown(title):
  """Generate markdown content based on the title by cloning a template."""
  if tags is None:
      tags = []
  if difficulty is None:
      difficulty = "Medium"
  
  slug = slugify(title)
  file_name = f"{slug}.md"
  file_path = Path("problems") / file_name

  Path("problems").mkdir(parents=True, exist_ok=True)
  
  shutil.copyfile(TEMPLATE_PATH, file_path)
  
  with open(file_path, 'r', encoding='utf-8') as file:
    content = file.read()
  
  content = content.replace("{{title}}", title)
  
  with open(file_path, 'w', encoding='utf-8') as file:
    file.write(content)
  
  return file_path

def create_markdown_file(title):
  """Create a markdown file with the generated content."""
  file_path = generate_markdown(title)
  print(f"Template created at: {file_path}")

def generate(title):
  create_markdown_file(title)