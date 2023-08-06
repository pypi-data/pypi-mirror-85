import sys
from typing import List, Dict

from tqdm import tqdm
from stockholm_data_manager.sterile.gsprd import Client, Gsprd, Spreadsheet, Worksheet, WorksheetNotFound, APIError

import stockholm_data_manager.constants as const
from stockholm_data_manager.sterile import time
from stockholm_data_manager.utils.logger import log


def write_cell_with_retries(worksheet: Worksheet, row, col, data, env=None):
    try:
        worksheet.update_cell(row, col, data)
    except APIError:
        log.info("Google sheets API quota hit. Sleeping for %ds.",
                 const.GOOGLE_READ_WRITE_COOLDOWN)
        time.sleep(const.GOOGLE_READ_WRITE_COOLDOWN, env=env)
        write_cell_with_retries(worksheet, row, col, data, env=env)


def setup_spreadsheet(spreadsheet: Spreadsheet,
                      worksheet_names: List[str],
                      rows: int,
                      columns: int) -> Dict[str, Worksheet]:
    """
    Create empty worksheets in the spreadsheet.

    ---------------------------------------------------------------------
    | WARNING: Deletes existing data in the spreadsheets!               |
    ---------------------------------------------------------------------

    - Clears every worksheet in the spreadsheet that has name in `worksheet_names`.
    - If the worksheet is not found, it is created.

    Args:
        spreadsheet (gspread.Spreadsheet): Google spreadsheet
        worksheet_names (List[str]): Names of the sheets that need to be reset.
        rows (int): Number of rows to be added in the worksheet.
        columns (int): Number of columns to be added in the worksheet.
    """
    worksheets = {}
    for worksheet_name in worksheet_names:
        try:
            spreadsheet.del_worksheet(worksheet_name)
        except WorksheetNotFound:
            log.info("Worksheet with name: %s was not found, creating.")
        finally:
            worksheets[worksheet_name] = spreadsheet.add_worksheet(title=worksheet_name,
                                                                   rows=rows,
                                                                   cols=columns)
    return worksheets


def slow__add_records(data: List[List[str]],
                      data_addition_offset: int,
                      label: str,
                      worksheets: Dict,
                      column_names: List[str],
                      env: str = None):
    """[summary]

    Args:
        data (List[List[str]]): [description]
        data_addition_offset (int): [description]
        label (str): [description]
        worksheets (Dict): [description]
        column_names (List[str]): [description]
        env (str, optional): [description]. Defaults to None.
    """
    log.debug("Working on %s.", label)
    for row_index, row in enumerate(data):
        for col_index, column_name in enumerate(column_names):
            if row_index == 0 and data_addition_offset == 0:
                write_cell_with_retries(worksheets[label],
                                        1, col_index + 1,
                                        column_name,
                                        env=env)
            write_cell_with_retries(worksheets[label],
                                    row_index + 2 + data_addition_offset,
                                    col_index + 1,
                                    row[col_index],
                                    env=env)


def slow__update_records(data: List[List[str]],
                         label: str,
                         index: int,
                         current_index_order: List[int],
                         worksheets: Dict,
                         column_names: List[str],
                         update_indices: List[int],
                         env: str = None):
    """[summary]

    Args:
        data (List[List[str]]): [description]
        index (int): [description]
        current_index_order (List[int]): [description]
        worksheets (Dict): [description]
        update_indices (List[int]): [description]
        n (int, optional): [description]. Defaults to GOOGLE_READ_WRITE_LIMIT.
        env (str, optional): [description]. Defaults to None.
    """
    log.debug("Working on %s.", label)
    for row_index, row in enumerate(data):
        for col_index in update_indices:
            write_cell_with_retries(worksheets[label],
                                    row_index + 2,
                                    col_index + 1,
                                    row[col_index],
                                    env=env)


def get_worksheets(spreadsheet: Spreadsheet, worksheet_names: List[str]):
    worksheets = {}
    for worksheet_name in worksheet_names:
        try:
            worksheets[worksheet_name] = spreadsheet.worksheet(worksheet_name)
        except WorksheetNotFound:
            log.error("Worksheet with name: %s was not found.", worksheet_name)
            sys.exit(0)
    return worksheets


def slow__sync_data2sheets(gsprd: Gsprd,
                           data: Dict,
                           spreadsheet_id: str,
                           worksheet_names: str,
                           column_names: str,
                           sheet_index: int,
                           update_indices: List[int]):
    """[summary]

    Args:
        gsprd (Gsprd): [description]
        data (Dict): [description]
        spreadsheet_id (str): [description]
        worksheet_names (str): [description]
        column_names (str): [description]
        sheet_index (int): [description]
        update_indices (List[int]): [description]
    """
    spreadsheet: Spreadsheet = gsprd.open_by_key(spreadsheet_id)
    worksheets: Dict[str, Worksheet] = get_worksheets(
        spreadsheet, worksheet_names)
    for worksheet_name in data:
        worksheet: Worksheet = worksheets[worksheet_name]
        current_index_order = worksheet.col_values(1)[1:]
        # We are sorting data so that the index values match exactly as in sheets.
        # There is a good chance that data will have index values that weren't there in the sheets.
        # in this case we want them to rank anywhere after the existing records.
        #
        # example:
        # current_index_order = [1, 2, 3, 4]
        # data = [[1, "a"], [5, "c"], [21, "y"], [3, "aa"], [2, "f"], [4, "z"], [10, "xx"]]
        # then, the line below does:
        # sort_by_index = [[1, 'a'], [2, 'f'], [3, 'aa'], [4, 'z'], [5, 'c'], [21, 'y'], [10, 'xx']]
        sort_by_index = sorted(data[worksheet_name], key=lambda el: current_index_order.index(
            el[0]) if el[0] in current_index_order else len(current_index_order))
        items_to_update = sort_by_index[:len(current_index_order)]
        items_to_add = sort_by_index[len(current_index_order):]
        slow__update_records(items_to_update,
                             worksheet_name,
                             sheet_index - 1,
                             current_index_order,
                             worksheets,
                             column_names,
                             update_indices,
                             env=gsprd.env)
        data_addition_offset = len(items_to_update)
        slow__add_records(items_to_add, data_addition_offset,  worksheet_name, worksheets,
                          column_names, env=gsprd.env)
