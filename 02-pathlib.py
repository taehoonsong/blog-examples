from pathlib import Path


def get_inputs() -> list[Path]:
    return [Path(item) for item in Path("input.txt").read_text("utf-8").splitlines()]


def create_files(data: list[Path]) -> None:
    for item in data:
        if item.parent != Path("."):
            item.parent.mkdir(exist_ok=True)

        if item.suffix == "":
            item.mkdir(exist_ok=True)
        else:
            item.touch()


def cleanup() -> None:
    test_files = Path(".").rglob("test*")

    # Delete files first
    for item in test_files:
        if item.is_file():
            item.unlink()

    test_dirs = Path(".").rglob("test*")
    for item in test_dirs:
        item.rmdir()


def main() -> None:
    data = get_inputs()

    if data is None:
        return

    print("Creating files...")
    create_files(data)
    _ = input("Press enter to clean up files.")
    cleanup()
    print("Deleted all test files.")


if __name__ == "__main__":
    main()
