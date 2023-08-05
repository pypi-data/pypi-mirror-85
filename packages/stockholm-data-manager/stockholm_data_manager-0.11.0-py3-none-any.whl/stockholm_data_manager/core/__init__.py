import os
import json
import re
from typing import List, Dict, Optional

import pandas as pd
from tqdm import tqdm
from gspread.client import Client
from gspread.exceptions import APIError

import stockholm_data_manager.constants as const
from stockholm_data_manager.sterile.gsprd import Gsprd, WorksheetNotFound, Spreadsheet, Worksheet
from stockholm_data_manager.sterile import time
from stockholm_data_manager.utils import train_test_split
from stockholm_data_manager.utils.logger import log, set_log_level


SUPPORTED_SOURCES = ["json"]


def clear_sheet_and_write(spreadsheet, worksheet_name, data_range, values, env=None):
    try:
        worksheet = spreadsheet.worksheet(worksheet_name)
        worksheet.clear()
        worksheet.update(data_range, values)
    except WorksheetNotFound:
        worksheet = spreadsheet.add_worksheet(
            title=worksheet_name, rows=3000, cols=15)
        worksheet.update(data_range, values)
    except APIError as e:
        log.debug(e)
        log.debug("Google sheets API quota hit. Sleeping for %ds.",
                  const.GOOGLE_READ_WRITE_COOLDOWN)
        time.sleep(const.GOOGLE_READ_WRITE_COOLDOWN, env=env)
        clear_sheet_and_write(spreadsheet, worksheet_name,
                              data_range, values, env=env)


class SDM:
    SHEET_TRAIN_DATASET = "sheet_train_dataset"
    SHEET_TEST_DATASET = "sheet_test_dataset"
    GENERATED_DATASET = "generated_dataset"
    LOCAL = "local"
    REMOTE = "sheet"
    DATA_LOCATIONS = [LOCAL, REMOTE]
    SHEET_TYPES = sorted([
        SHEET_TRAIN_DATASET,
        SHEET_TEST_DATASET,
        GENERATED_DATASET
    ])

    def __init__(self,
                 credentials_file: str,
                 local_dataset_path: str,
                 metrics_path: str,
                 spreadsheets_map: str,
                 from_version: str,
                 to_version: str,
                 index_column: str,
                 column_names: List[str],
                 worksheet_names: List[str],
                 env: str = None,
                 log_level="DEBUG"):
        set_log_level(log_level)
        # This environment tells if the module is to be used for tests or actual use.
        self.env = env

        # This is the version of local dataset that should be incremented.
        self.from_version = from_version

        # This is the version of local dataset that is created after increments.
        self.to_version = to_version

        # This is the location where we want to reference an existing dataset over which we will increment new data
        # from various sources.
        self.local_dataset_path = local_dataset_path

        # updated dataset with model predictions, confidence etc lie here.
        self.metrics_path = metrics_path

        # Mocked gspread
        self.gsprd = Gsprd(env)

        # Google auth credentials file
        self.credentials_file: str = credentials_file

        # gspread.client.Client Credentials object.
        self.credentials: Optional[Client] = None

        # Spreadsheet example config:
        # {
        #     "en": {
        #         "sheet_train_dataset": "<sheet_id>",
        #         "sheet_test_dataset": "<sheet_id>",
        #         "generated_dataset": "<sheet_id>"
        #     }
        # }
        self.spreadsheets: Dict = spreadsheets_map
        # List of supported language codes, eg: ['en', ...]

        self.index_column: str = index_column
        # Column names for worksheets.
        self.column_names: List[str] = column_names

        # Worksheet names to be created under spreadsheets.
        self.worksheet_names: List[str] = worksheet_names
        self.__service_account_auth()
        self.__validate_spreadsheets()

    def __service_account_auth(self):
        """
        Use google service account credentials to access spreadsheets.
        """
        if not self.credentials:
            self.credentials = self.gsprd.service_account(
                filename=self.credentials_file
            )

    def __col2index(self, col_name: str) -> Optional[int]:
        """
        Get google sheets indexing for column name

        Say column name is index 0, on google sheets it would be referenced as 1.

        Args:
            col_name (str): A column in a worksheet.

        Returns:
            Optional[int]: int if column exists in the worksheet, else None.
        """
        if col_name in self.column_names:
            return self.column_names.index(col_name) + 1
        return None

    def __validate_spreadsheets(self) -> None:
        """
        Verify spreadsheets config is valid.

        This method will raise exceptions if self.spreadsheets is not appropriate.

        Raises:
            ValueError
            TypeError
        """
        if not self.spreadsheets:
            raise ValueError("Spreadsheets are not initialized.")

        # Check if the languages to support have associated spreadsheet config.
        spreadsheet_languages = sorted(self.spreadsheets.keys())

        for language in spreadsheet_languages:
            spreadsheet_types = sorted(self.spreadsheets[language].keys())
            # There are 3 types of spreadsheets supported per-language.
            # We check if everything matches.
            if spreadsheet_types != self.SHEET_TYPES:
                raise ValueError("Sheet types expected: %s, found %s.",
                                 self.SHEET_TYPES, spreadsheet_types)

            # Type of spreadsheet ids should be string
            for spreadsheet_type in self.spreadsheets[language]:
                if not isinstance(self.spreadsheets[language][spreadsheet_type], str):
                    raise TypeError("Spreadsheet id(s) are expected to be of type str but %s was found for %s %s.", type(
                        type(self.spreadsheets[language][spreadsheet_type]), language, spreadsheet_type))

    def __get_spreadsheet_id(self, language: str, sheet_type: str) -> str:
        """
        Get spreadsheet id from spreadsheet config.

        Args:
            language (str): Language code of spreadsheet.
            sheet_type (str): A sheet type, refer to `self.SHEET_TYPES`.

        Returns:
            str: Spreadsheet-id that can be used to access the google sheet.
        """
        if self.spreadsheets:
            return self.spreadsheets[language.lower()][sheet_type.lower()]
        return None

    def add_new_data_to_local_dataset(self, df, langauge, sheet_type):
        save_path = os.path.join(self.local_dataset_path,
                                 self.to_version,
                                 langauge)
        os.makedirs(save_path, exist_ok=True)
        df.to_csv(os.path.join(save_path, f"{sheet_type}.csv"), index=False)

    def read_worksheet_data(self, spreadsheet, worksheet_name, delete=False):
        records = []
        try:
            worksheet: Worksheet = spreadsheet.worksheet(
                worksheet_name)
            records = worksheet.get_all_records()
            if delete:
                spreadsheet.del_worksheet(worksheet)
            return records
        except APIError as e:
            error_message = str(e)
            if re.search(r"Sheet with name: .* not found", error_message):
                log.debug(error_message)
            elif re.search(r"Unable to parse range:", error_message):
                log.debug(error_message)
            elif re.search(r"RESOURCE_EXHAUSTED", error_message):
                log.info("Google sheets API quota hit. Sleeping for %ds.",
                         const.GOOGLE_READ_WRITE_COOLDOWN)
                time.sleep(const.GOOGLE_READ_WRITE_COOLDOWN, env=self.env)
                return self.read_worksheet_data(spreadsheet,
                                                worksheet_name,
                                                delete=delete)
            else:
                raise APIError(e)

    def read_all_sheets_in_spreadsheet(self, spreadsheet, delete=False):
        worksheets = []
        for worksheet_name in tqdm(self.worksheet_names):
            try:
                worksheet_data = self.read_worksheet_data(
                    spreadsheet, worksheet_name, delete)
                if worksheet_data:
                    worksheets.append(worksheet_data)
                log.debug("Adding %d data points from sheet with name: %s.",
                          len(worksheet_data),
                          worksheet_name)
            except WorksheetNotFound:
                log.debug("Sheet with name: %s not found.", worksheet_name)
        worksheet_dataset = [row
                             for worksheet in worksheets
                             for row in worksheet]
        log.info("Added %d data points.", len(worksheet_dataset))
        return worksheet_dataset

    def add_generated_data(self, language: str, worksheet_name: str, data: List[str]):
        if language not in self.spreadsheets:
            raise ValueError(
                f"{language} is not valid. Pick from {self.spreadsheets.keys()}.")

        if worksheet_name not in self.worksheet_names:
            raise ValueError(
                f"{worksheet_name} is not valid. Pick from {self.worksheet_names}.")

        if len(self.column_names) != len(data):
            raise ValueError(
                f"Number of columns is {len(self.column_names)} but data with {len(data)} columns was found.")

        data_generation_sheet = self.gsprd.open_by_key(
            self.spreadsheets[language][self.GENERATED_DATASET]
        )

        try:
            worksheet = data_generation_sheet.worksheet(worksheet_name)
        except WorksheetNotFound:
            worksheet = data_generation_sheet.add_worksheet(
                title=worksheet_name, rows=3000, cols=15)
            worksheet.append_row(self.column_names)
        return worksheet.append_row(data)

    def sync_sheets2local(self, language: str, test_ratio: float = 0.3):
        """[summary]

        Args:
            language (str): [description]
        """
        # Gather spreadsheet ids for all types of data sources on google-sheets and
        # load a reference.
        data_generation_sheet: Spreadsheet = self.gsprd.open_by_key(
            self.spreadsheets[language][self.GENERATED_DATASET]
        )
        training_sheet: Spreadsheet = self.gsprd.open_by_key(
            self.spreadsheets[language][self.SHEET_TRAIN_DATASET]
        )
        testing_sheet: Spreadsheet = self.gsprd.open_by_key(
            self.spreadsheets[language][self.SHEET_TEST_DATASET]
        )

        # Read all worksheets in the data generation spreadsheet
        log.info("Load generated data from sheet source: %s.",
                 self.spreadsheets[language][self.GENERATED_DATASET])
        generated_data = self.read_all_sheets_in_spreadsheet(
            data_generation_sheet, delete=True)
        log.debug("Fetched %d items.", len(generated_data))

        log.info("Refresh training data from sheet source: %s.",
                 self.spreadsheets[language][self.SHEET_TRAIN_DATASET])
        current_training_data = self.read_all_sheets_in_spreadsheet(
            training_sheet)

        log.info("Refresh updated test data from sheet source: %s.",
                 self.spreadsheets[language][self.SHEET_TEST_DATASET])
        current_testing_data = self.read_all_sheets_in_spreadsheet(
            testing_sheet)

        train_data = []
        test_data = []
        if generated_data:
            generated_data_dfs = pd.DataFrame(generated_data,
                                              columns=self.column_names)

            train_data, test_data = train_test_split.split(
                generated_data_dfs, test_ratio=test_ratio
            )

        total_train_data = pd.DataFrame(train_data + current_training_data,
                                        columns=self.column_names)
        total_test_data = pd.DataFrame(test_data + current_testing_data,
                                       columns=self.column_names)

        self.add_new_data_to_local_dataset(total_train_data, language, "train")
        self.add_new_data_to_local_dataset(total_test_data, language, "test")

    def sync_local_data2sheets(self, language: str, sheet_type: str):
        if sheet_type == self.SHEET_TEST_DATASET:
            spreadsheet: Spreadsheet = self.gsprd.open_by_key(
                self.spreadsheets[language][self.SHEET_TEST_DATASET]
            )
            local_name = "test_error_records.json"
        if sheet_type == self.SHEET_TRAIN_DATASET:
            spreadsheet: Spreadsheet = self.gsprd.open_by_key(
                self.spreadsheets[language][self.SHEET_TRAIN_DATASET]
            )
            local_name = "train_error_records.json"

        local_data_path = os.path.join(
            self.metrics_path,
            self.from_version,
            language,
            local_name
        )

        with open(local_data_path, "r", encoding="utf-8") as f:
            local_data = json.load(f)

        for worksheet_name, values in tqdm(local_data.items()):
            values.insert(0, self.column_names)
            data_range = "A1"
            log.debug(worksheet_name)
            log.debug("Adding: %d rows to range: %s", len(values), data_range)
            clear_sheet_and_write(spreadsheet,
                                  worksheet_name,
                                  data_range,
                                  values, env=self.env)

    def sync_local2sheets(self, language: str):
        # Gather spreadsheet ids for all types of data sources on google-sheets and
        # load a reference.
        log.info("Copying data to test sheet.")
        self.sync_local_data2sheets(language, self.SHEET_TEST_DATASET)

        log.info("Copying data to train sheet.")
        self.sync_local_data2sheets(language, self.SHEET_TRAIN_DATASET)
