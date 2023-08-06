import os
import itertools
import re

from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import click
from filetype import guess

from ..services.requests import extract_invoice, validation, validate_vat


def run_requests(workers: int, path: str, services) -> dict:
    files = get_filenames(path)
    result, vat_validation_result = {}, {}

    with ThreadPoolExecutor(max_workers=workers) as exe:
        jobs = {
            exe.submit(
                extract_invoice,
                read_pdf(file_path),
                services.extractor_endpoint,
                file_extension,
                services.get_token,
                services.headers,
            ): file_path
            for file_path, file_extension in files.items()
        }
        label = f"Converting {len(jobs)} invoices"

        with click.progressbar(jobs, label=label) as bar:
            for idx, future in enumerate(as_completed(jobs)):
                file_name = jobs[future].split("/")[-1]
                validated_invoice = None

                try:
                    extracted_invoice = future.result(timeout=300)

                    if getattr(services, "validation_endpoint", None):
                        validated_invoice = validation(
                            extracted_invoice, services.validation_endpoint
                        )

                    if getattr(services, "vat_validation_endpoint", None):
                        vat_validation_result[idx] = validate_vat(
                            extracted_invoice, services.vat_validation_endpoint
                        )
                        vat_validation_result[idx]["file_name"] = file_name

                    result[idx] = flatten_invoice(extracted_invoice, validated_invoice,)
                except Exception as e:
                    result[idx] = {"error_message": (str(e), None, None)}
                finally:
                    result[idx]["file_name"] = (file_name, None, None)

                bar.update(1)

    if not result:
        quit("No files found in path")
    return (result, vat_validation_result)


def flatten_invoice(invoice, validation):
    return_dict = dict()
    entities = invoice["entities"]
    probabilities = invoice.get("probabilities")

    def traverse_items(entities, probabilities, validation, _dict, *prefix):
        for k, v in entities.items():
            if isinstance(v, dict):
                traverse_items(
                    entities[k],
                    probabilities[k] if probabilities else None,
                    validation[k][0] if validation and k in validation else None,
                    return_dict,
                    k,
                )
            elif isinstance(v, list):
                # items, taxes, terms
                if all(isinstance(list_item, dict) for list_item in v):
                    for counter, list_item in enumerate(v):
                        temp_dict = {}
                        for item, value in list_item.items():
                            temp_dict[f"{k}_{item}_{counter}"] = value
                        traverse_items(
                            temp_dict,
                            probabilities[k][counter] if probabilities else None,
                            validation[k][0][str(counter)][0]
                            if validation
                            and k in validation
                            and str(counter) in validation[k][0]
                            else None,
                            return_dict,
                        )
                # ibanAll enc
                elif all(isinstance(list_item, str) for list_item in v):
                    if v:
                        _dict[k] = []
                        for _, list_item in enumerate(v):
                            _dict[k].append(list_item)
                        _dict[k] = (", ".join(_dict[k]), None, None)
                    else:
                        _dict[k] = ("", None, None)
                # Undefined datastructure
                else:
                    pass
            else:
                try:
                    # dirty solution, assumes no invoice extractor response field got underscore
                    original_k = k.split("_")[-2]
                except IndexError:
                    original_k = k

                if prefix:
                    field_name = f"{prefix[0]}_{k}"
                else:
                    field_name = k

                if probabilities and original_k in probabilities:
                    if probabilities[original_k]:
                        _dict[field_name] = (
                            v if v else "",
                            probabilities[original_k],
                            None,
                        )
                    else:
                        _dict[field_name] = (v if v else "", None, None)
                else:
                    _dict[field_name] = (v if v else "", None, None)
                if validation:
                    if original_k in validation:
                        _dict[field_name] = (
                            v if v else "",
                            None,
                            validation[original_k],
                        )

    traverse_items(entities, probabilities, validation, return_dict)
    return return_dict


def read_pdf(pdf_path: str) -> bytes:
    with open(pdf_path, "rb") as pdf:
        pdf = pdf.read()

    return pdf


def get_filenames(path: str) -> list:
    types = ("*.pdf", "*.tif", "*.tiff", "*.png", "*.jpg")
    abs_path = os.path.join(os.getcwd(), path)
    files_grabbed = []

    for files in types:
        files_grabbed.extend(Path(abs_path).rglob(files))
        files_grabbed.extend(Path(abs_path).rglob(files.upper()))

    files_grabbed = [str(f) for f in files_grabbed]
    return {f: guess(f).mime for f in files_grabbed if guess(f).mime}


def structure_sheets(response: dict, header_sheetname="header"):
    """Structure the extracted invoices in different sheets.

    Arguments:
        response {[type]} -- [description]

    Returns:
        [type] -- [description]
    """
    single_cardinality = {header_sheetname: []}
    multi_cardinality = {}

    for idx, document in response.items():
        single_cardinality[header_sheetname].append(
            {
                "file_name": document["file_name"],
                "error_message": document.get("error_message", (None, None, None)),
            }
        )
        multi_items = {}

        for col, value in document.items():
            if col[-1].isdigit():
                item_num = int(col.split("_")[-1])
                label = col.split("_")[1]
                category = col.split("_")[0]
                multi_items.setdefault(category, [])

                if len(multi_items[category]) == item_num:
                    multi_items[category].append(
                        {
                            "file_name": document["file_name"],
                            "row_number": (item_num + 1, None, None),
                        }
                    )

                multi_items[category][item_num][label] = document[col]
            else:
                single_cardinality[header_sheetname][idx][col] = document[col]

        for category, rows in multi_items.items():
            for row in rows:
                multi_cardinality.setdefault(category, []).append(row)

    return {**single_cardinality, **multi_cardinality}


def get_output_path(input_path, output_path, extension="xlsx"):
    if not output_path:
        if input_path == ".":
            output_path = f"hycli.{extension}"
        else:
            output_path = (
                f"{os.path.normpath(input_path).split(os.path.sep)[-1]}.{extension}"
            )
    else:
        output_path = f"{os.path.join(os.getcwd(), output_path)}"
        if not os.path.isdir(os.path.sep.join(output_path.split(os.path.sep)[:-1])):
            quit("Output directory does not exist")

    return output_path


def structure_sheet(records):
    columns = set()

    # Collect all column names
    for record in records:
        columns = columns.union(set(record.keys()))

    for idx, record in enumerate(records.copy()):
        # Insert all missing columns into record
        record.update(
            {k: (None, None, None) for k in columns if k not in record.keys()}
        )

        # All snake_case keys
        record = {
            re.sub(r"(?<!^)(?=[A-Z])", "_", k).lower(): v for k, v in record.items()
        }

        # Reorder column order
        if "error_message" in record or "row_number" in record:
            records[idx] = {
                **dict(itertools.islice(record.items(), 2)),
                **dict(sorted(itertools.islice(record.items(), 2, None))),
            }
        else:
            records[idx] = {
                **dict(itertools.islice(record.items(), 1)),
                **dict(sorted(itertools.islice(record.items(), 1, None))),
            }

    return records
