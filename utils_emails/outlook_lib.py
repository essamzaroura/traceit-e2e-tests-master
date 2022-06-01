import os

import win32com.client

class OutlookLib:

    def __init__(self, user_email):
        self.outlook = win32com.client.Dispatch("Outlook.Application")
        self.user_email = user_email

    def open(self):
        os.startfile("outlook")

    def close(self):
        self.outlook.Quit()

    def get_messages(self, folder="Inbox", restrict_query=None):
        """
        Returns all the messages from the specified folder.
        :param folder: A string, representing an Outlook Folder to get messages from.
        :param restrict_query: a query string allowing to filter the messages.
            Docs: https://docs.microsoft.com/en-us/office/vba/api/outlook.items.restrict
        :return A list of Items collection Object representing email messages
        """
        outlook = self.outlook.GetNamespace("MAPI")
        myfolder = outlook.Folders[self.user_email]
        inbox = myfolder.Folders[folder]
        if not restrict_query:
            return inbox.Items
        return inbox.Items.Restrict(restrict_query)

    def get_body(self, msg):
        return msg.Body

    def get_subject(self, msg):
        return msg.Subject

    def get_sender(self, msg):
        if msg.SenderEmailType == "EX":
            sender = msg.Sender.GetExchangeUser().PrimarySmtpAddress
        else:
            sender = msg.SenderEmailAddress
        return sender

    def get_recipient(self, msg):
        return msg.To

    def get_attachments(self, msg):
        return msg.Attachments

    def find_latest_message(self, msgs):
        return msgs.GetLast()
