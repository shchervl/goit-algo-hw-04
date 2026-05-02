import argparse
import shutil
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Recursively copy files sorted by extension."
    )
    parser.add_argument("source", type=Path, help="Source directory")
    parser.add_argument(
        "destination", type=Path, nargs="?", default=None,
        help="Destination directory (default: dist)",
    )
    return parser.parse_args()


def validate_source(source: Path) -> str | None:
    if not source.is_dir():
        return f"Provided source is not a directory: {source}"
    return None


def get_extension(file: Path) -> str:
    return file.suffix[1:].lower() or "no_extension"


def copy_file(file: Path, destination: Path, created_dirs: set) -> None:
    target_dir = destination / get_extension(file)
    if target_dir not in created_dirs:
        target_dir.mkdir(parents=True, exist_ok=True)
        created_dirs.add(target_dir)
    shutil.copy2(file, target_dir / file.name)


def traverse(source: Path, destination: Path, dest_resolved: Path, created_dirs: set) -> None:
    for item in source.iterdir():
        try:
            if item.resolve() == dest_resolved:
                continue
            if item.name.startswith("."):
                continue
            if item.is_dir():
                traverse(item, destination, dest_resolved, created_dirs)
            elif item.is_file():
                copy_file(item, destination, created_dirs)
        except PermissionError as e:
            print(f"Access denied: {e}")
        except OSError as e:
            print(f"Error processing {item}: {e}")


def main() -> None:
    args = parse_args()
    destination = args.destination or Path("dist")

    error = validate_source(args.source)
    if error:
        print(error)
        return

    destination.mkdir(parents=True, exist_ok=True)
    traverse(args.source, destination, destination.resolve(), set())
    print(f"Done. Files are copied to: {destination}")


if __name__ == "__main__":
    main()
