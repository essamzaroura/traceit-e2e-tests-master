import re
import datetime as dt
from utils_emails.outlook_lib import OutlookLib


class EmailHandler:

    def __init__(self, email_address):
        self.outlook = OutlookLib(email_address)

    def get_content_from_latest_in_drafts(self):
        received_time = (dt.datetime.now() - dt.timedelta(minutes=10)).strftime('%m/%d/%Y %H:%M %p')
        messages = self.outlook.get_messages(folder='Drafts', restrict_query=f"[ReceivedTime] >= '{received_time}'")
        if not len(messages):
            raise Exception("Messages not found in Drafts")
        latest_message = self.outlook.find_latest_message(messages)
        latest_message = self.outlook.get_body(latest_message)
        content = self._clean_up(latest_message)
        return content

    def open_outlook(self):
        self.outlook.open()

    def close_outlook(self):
        self.outlook.close()

    def _clean_up(self, str):
        _RE_COMBINE_WHITESPACE = re.compile(r"\s+")
        str = _RE_COMBINE_WHITESPACE.sub("", str).strip()
        return str
