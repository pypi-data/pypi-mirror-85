import json
from typing import Union

class OnlineAssignmentQuestionContent:
    def __init__(self, *args, **kwargs):
        pass

    def jsonify(self):
        pass

class OnlineAssignmentQuestionContentText(OnlineAssignmentQuestionContent):
    def __init__(self, value=""):
        self.set_value(value)
    
    def set_value(self, value):
        self.value = value

    def get_value(self):
        return self.value

    def jsonify(self):
        return {"type": "text", "value": self.value}

class OnlineAssignmentQuestionContentFileUpload(OnlineAssignmentQuestionContent):
    def __init__(self):
        pass

    def jsonify(self):
        return {"type": "file_upload_input"}

class OnlineAssignmentQuestionContentTextInput(OnlineAssignmentQuestionContent):
    def __init__(self, answer: str="answer"):
        self.set_answer(answer)
    
    def set_answer(self, answer: str):
        self.answer = answer

    def get_answer(self):
        return self.answer

    def jsonify(self):
        return {"type": "text_input", "answer": ""}

class OnlineAssignmentQuestionContentFreeResponseInput(OnlineAssignmentQuestionContent):
    def __init__(self):
        pass

    def jsonify(self):
        return {"type": "free_response_input"}

class OnlineAssignmentQuestionChoices:
    def __init__(self, value: str="", answer: bool=False):
        self.value = value
        self.answer = answer

    def jsonify(self):
        return {"value": self.value, "answer": self.answer}

class OnlineAssignmentQuestionContentRadioInput(OnlineAssignmentQuestionContent):
    def __init__(self, choices: [OnlineAssignmentQuestionChoices]):
        self.choices = []
        for choice in choices:
            self.add_choice(choice)

    def add_choice(self, choice):
        self.choices.append(choice)

    def remove_choice(self, choice):
        self.choices.remove(choice)

    def jsonify(self):
        return {"type": "radio_input", "choices": [c.jsonify() for c in self.choices]}

class OnlineAssignmentQuestionContentSelectAllInput(OnlineAssignmentQuestionContentRadioInput):
    def jsonify(self):
        return {"type": "select_all_input", "choices": [c.jsonify() for c in self.choices]}



class OnlineAssignmentQuestion:
    def __init__(self, id: int=None, title: str="", parent_id: Union["OnlineAssignmentQuestion", str]="None", index: int=1, weight: float=1.0, content: [OnlineAssignmentQuestionContent] = []):
        pass

class OnlineAssignmentQuestionGroup:
    pass

class GS_online_assignment:
    def __init__(self, client: "GradescopeClient", class_id: str, assignment_id: str):
        self.client = client
        self.class_id = class_id
        self.assignment_id = assignment_id
        self.questions = []
        self.last_outline = None
        self.last_sub_info = None

    def _update_outline(self, outline: str):
        return self.client.update_online_assignment(self.class_id, self.assignment_id, outline)

    def _get_outline(self, repull=False):
        if repull or self.last_outline is None:
            self.last_outline = json.loads(self.client.get_online_assignment_outline(self.class_id, self.assignment_id))
        return self.last_outline

    def _get_new_submission_info(self, repull=False):
        if repull or self.last_sub_info is None:
            self.last_sub_info = json.loads(self.client.get_online_assignment_new_submission(self.class_id, self.assignment_id))
        return self.last_sub_info

    def _get_roster(self) -> dict:
        sub_data = self._get_new_submission_info()
        DICT_ID = "roster"
        if DICT_ID in sub_data:
            return sub_data[DICT_ID]

    def get_roster_by_email(self):
        roster = self._get_roster()
        if not roster:
            print(f"[ERROR]: Failed to get roster!")
            return
        email_roster = {}
        EMAIL_ID = "email"
        for std in roster:
            if std[EMAIL_ID] in email_roster:
                print(f"ERROR STUDENT EMAIL ALREADY IN ROSTER: {std}")
                continue
            email_roster[std[EMAIL_ID]] = std
        return email_roster

    def _make_new_submission(self, email: str, data: Union[dict, str]) -> bool:
        if isinstance(data, dict):
            data = json.dumps(data)
        email_roster = self.get_roster_by_email()
        if not email_roster:
            print(f"[ERROR]: Failed to get roster!")
            return False
        if email not in email_roster:
            print(f"[ERROR]: Could not find the email {email} in the roster!")
            return False
        owner_id = email_roster[email]['id']
        return self.client.submit_online_assignment(self.class_id, self.assignment_id, owner_id, data)
