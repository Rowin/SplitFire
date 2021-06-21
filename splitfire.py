import yaml
from PyPDF2 import PdfFileWriter, PdfFileReader  # type: ignore
import os

DEFAULT_OPTIONS = {"subfolder": False, "subfolder_suffix": "folder"}


def get_split_intervals(split_positions: list, length: int) -> list[list[int]]:
    """Returns page intervals from position where to split

    - split_positions: list of pages where to split. The split occurs BEFORE the page.
        For example, split at page 3 on 5 pages document will give [1, 2], [3, 4, 5]
    - length: length of the document, in pages
    """
    intervals = []
    remaining_pages = list(range(1, length + 1))
    for position in split_positions:
        i = remaining_pages.index(position)
        intervals.append(remaining_pages[:i])
        remaining_pages = remaining_pages[i:]
    intervals.append(remaining_pages)

    return intervals


def get_config(filename: str) -> tuple[dict, dict]:
    with open(filename, "r") as config_file:
        config = yaml.load(config_file)

        files_config = config["files"]
        options_dict = DEFAULT_OPTIONS | config["options"]

        return files_config, options_dict


def split_file(file_config: dict, options: dict) -> None:
    with open(file_config["name"], "rb") as infile:
        inputpdf = PdfFileReader(infile)

        folder_name = ""
        if options["subfolder"]:
            filename, _ = os.path.splitext(file_config["name"])
            folder_name = f'{filename}_{options["subfolder_suffix"]}'
            os.mkdir(folder_name)

        split_intervals = get_split_intervals(file_config["split"], inputpdf.numPages)
        for interval, outfilename in zip(split_intervals, file_config["sub_files"]):
            outfilename = os.path.join(folder_name, outfilename)
            export_page_range(inputpdf, interval, outfilename)


def export_page_range(
    inputpdf: PdfFileReader, interval: list[int], outfilename: str
) -> None:
    outputpdf = PdfFileWriter()
    for page in interval:
        outputpdf.addPage(inputpdf.getPage(page - 1))

    with open(outfilename, "wb") as outfile:
        outputpdf.write(outfile)


def main(config_filename: str) -> None:
    files_config, options = get_config(config_filename)

    for file_config in files_config:
        split_file(file_config, options)


if __name__ == "__main__":
    main("config.yaml")
