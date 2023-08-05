from typing import Union, List
import gspread


class MockWorksheet:
    def __init__(self, name):
        self.name = name

    def append_row(self, data: List[str]):
        return True

    def update(self, address: str, data: List):
        return True

    def update_cell(self, row: int, col: int, data: str):
        return True

    def get_all_records(self):
        return []

    def col_values(self, index):
        return []

    def row_values(self, index):
        return []


Worksheet = Union[gspread.Worksheet, MockWorksheet]


class MockSpreadsheet:
    def worksheet(self, sheet_name):
        return Worksheet(sheet_name)

    def del_worksheet(self, sheet_name):
        return True

    def add_worksheet(self, title="", rows=0, cols=0):
        return MockWorksheet(title)


class MockCreds:
    pass


Client = Union[gspread.client.Client, MockCreds]
Spreadsheet = Union[gspread.Spreadsheet, MockSpreadsheet]
WorksheetNotFound = gspread.exceptions.WorksheetNotFound
APIError = gspread.client.APIError


class Gsprd:
    def __init__(self, env):
        self.env = env
        self.credentials = MockCreds()
        self.spreadsheet = MockSpreadsheet()

    def service_account(self, filename: str) -> Client:
        if self.env != "test":
            self.credentials = gspread.service_account(filename)
        return self.credentials

    def open_by_key(self, spreadsheet_id) -> Spreadsheet:
        if self.env != "test":
            self.spreadsheet = self.credentials.open_by_key(spreadsheet_id)
        return self.spreadsheet
