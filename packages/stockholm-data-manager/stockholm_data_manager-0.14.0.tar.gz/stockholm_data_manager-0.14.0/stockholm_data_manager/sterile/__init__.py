"""
This module is for mocking methods that can hinder testing.
API calls, timeouts etc that are either costly, time-consuming or not required for passing tests.

module mocked: reason
- gspread: Success/Failrue of API calls to google sheets are not part of this project.
- time: time.sleep(n) is not required during tests.
"""
