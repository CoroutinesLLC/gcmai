import os
from pathlib import Path


def parse_gitignore():
    gitignore_path = Path(".gitignore")
    ignore_patterns = []
    if gitignore_path.exists():
        with open(gitignore_path, "r") as f:
            ignore_patterns = [
                line.strip() for line in f if line.strip() and not line.startswith("#")
            ]
    return ignore_patterns


def is_ignored(path, ignore_patterns):
    if path.name.startswith("."):
        return True
    for pattern in ignore_patterns:
        if path.match(pattern):
            return True
    return False


def find_files_recursively(root, ignore_patterns, file_starts_with):
    matching_files = []
    for dirpath, dirnames, filenames in os.walk(root):
        # Filter out directories and files that are ignored or start with a dot
        dirnames[:] = [
            d for d in dirnames if not is_ignored(Path(dirpath) / d, ignore_patterns)
        ]
        for file in filenames:
            if file.startswith(file_starts_with) and not is_ignored(
                Path(dirpath) / file, ignore_patterns
            ):
                matching_files.append(Path(dirpath) / file)
    return matching_files


def check_for_frameworks_in_file(file_name, frameworks):
    """Check if any framework is present in the given file."""
    if file_name.exists():
        with open(file_name, "r") as f:
            content = (
                f.read().lower()
            )  # Convert content to lowercase for easy searching
            for framework in frameworks:
                if framework in content:
                    return framework.capitalize()
    return None


def identify_python_framework():
    """Identify if Django, Flask, or FastAPI is present in the project."""
    frameworks = ["django", "fastapi", "flask"]

    # Get gitignore patterns
    ignore_patterns = parse_gitignore()

    # Find any requirements-like files or pyproject.toml
    requirements_files = find_files_recursively(".", ignore_patterns, "requirements")
    pyproject_files = find_files_recursively(".", ignore_patterns, "pyproject.toml")

    # Check for frameworks in requirements files and pyproject.toml
    for file in requirements_files + pyproject_files:
        framework = check_for_frameworks_in_file(file, frameworks)
        if framework:
            return f"{framework} project detected in {file}."

    return "No recognized framework detected."


def run_first_time_on_project():
    from pprint import pprint

    import inquirer

    questions = [
        inquirer.List(
            "project_type",
            message="What type of project do you have?",
            choices=["Django", "FastAPI", "Flask", "Other"],
        ),
    ]
    answers = inquirer.prompt(questions)
    pprint(answers)


def main():
    print("Hello, I'm gcmai!")
    # project_type = identify_python_framework()
    # if project_type == "No recognized framework detected.":
    #     run_first_time_on_project()
    # else:
    #     print("Framework detected:", project_type, "You are all set!")


if __name__ == "__main__":
    main()
