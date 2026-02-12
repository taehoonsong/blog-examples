import os
import contextlib


def get_inputs() -> list[str] | None:
    input_file = "input.txt"
    if not os.path.exists(input_file):
        print("Input file does not exist.")
        return None

    with open(input_file, "r", encoding="utf-8") as f:
        data = f.read().splitlines()

    return data


def create_file(file_name: str) -> None:
    with open(file_name, "a", encoding="utf-8"):
        pass


def create_files(data: list[str]) -> None:
    for item in data:
        if "/" not in item:
            create_file(item)
            continue

        # Assume only one level deep
        dir_name, file_name = item.split("/")
        with contextlib.suppress(FileExistsError):
            os.mkdir(dir_name)
        if file_name != "":
            create_file(item)


def cleanup(data: list[str]) -> None:
    for item in data:
        if "/" not in item:
            os.unlink(item)
            continue

        dir_name, _ = item.split("/")
        with contextlib.suppress(PermissionError):
            os.unlink(item)

        os.rmdir(dir_name)


def main() -> None:
    data = get_inputs()

    if data is None:
        return

    print("Creating files...")
    create_files(data)
    _ = input("Press enter to clean up files.")
    cleanup(data)
    print("Deleted all test files.")


if __name__ == "__main__":
    main()
