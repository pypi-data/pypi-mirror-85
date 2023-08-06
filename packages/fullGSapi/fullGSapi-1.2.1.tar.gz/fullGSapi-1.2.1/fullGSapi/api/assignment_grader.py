import csv
from io import StringIO
from io import BytesIO
import os
from .utils import extract_zip, is_float
import json
import enum

class GroupTypes(enum.Enum):
    complex = "complex"
    non_grouped = "non_grouped"
    mc = "mc"
    math = "math"
    words = "words"

class GS_assignment_Grader:
    def __init__(self, client, course_id, assignment_id):
        self.client = client
        self.course_id = course_id
        self.assignment_id = assignment_id
        self.last_scores = None
        self.last_eval_export = None
        self.email_to_sub_mapping = None
        self.sub_to_questions_mapping = None
        self.data = None # Extra variable for other programs to use

    def student_email_to_submission_ids(self, verbose: bool=False, force: bool=False) -> dict:
        if not self.last_scores or force:
            self.last_scores = self.client.download_scores(self.course_id, self.assignment_id)
        if self.last_scores:
            self.email_to_sub_mapping = {}
            reader = csv.DictReader(StringIO(self.last_scores.decode()))
            for row in reader:
                email = row.get("Email")
                sub_id = row.get("Submission ID")
                if not sub_id and verbose:
                    print(f"Submission ID is empty or could not be found! {row}")
                    continue
                if email:
                    if email not in self.email_to_sub_mapping:
                        self.email_to_sub_mapping[email] = sub_id
                    else:
                        if verbose:
                            print(f"Email already in email_to_sub_mapping! {row}")
                else:
                    if verbose:
                        print(f"Email is empty or could not find the email!")
            return self.email_to_sub_mapping
    
    def sub_id_to_questions_id(self, verbose: bool=False, force: bool=False) -> dict:
        if not self.last_eval_export or force:
            self.last_eval_export = self.client.export_evaluations(self.course_id, self.assignment_id)
        if self.last_eval_export:
            self.sub_to_questions_mapping = {}
            files = extract_zip(BytesIO(self.last_eval_export))
            for question, data in files.items():
                base = os.path.basename(question)
                question_id_and_name = os.path.splitext(base)[0]
                question_id = question_id_and_name.split("_")[0]
                reader = csv.DictReader(StringIO(data.decode()))
                for row in reader:
                    sub_id = row.get("Assignment Submission ID")
                    q_sub_id = row.get("Question Submission ID")
                    if sub_id and q_sub_id and is_float(sub_id) and is_float(q_sub_id):
                        if sub_id not in self.sub_to_questions_mapping:
                            self.sub_to_questions_mapping[sub_id] = {}
                        self.sub_to_questions_mapping[sub_id][question_id] = q_sub_id
            return self.sub_to_questions_mapping
    
    def email_to_qids(self, email_to_sub: dict=None, sub_to_q: dict = None, verbose: bool=False, force: bool=False) -> dict:
        if not email_to_sub:
            email_to_sub = self.student_email_to_submission_ids(verbose=verbose, force=force)
        if not sub_to_q:
            sub_to_q = self.sub_id_to_questions_id(verbose=verbose, force=force)
        emails_to_qids_dict = {}
        for email, sub_id in email_to_sub.items():
            if sub_id in sub_to_q:
                emails_to_qids_dict[email] = sub_to_q[sub_id]
        return emails_to_qids_dict

    def get_outline(self) -> "GS_Outline":
        raw_data = self.client.get_assignment_outline(self.course_id, self.assignment_id)
        if raw_data:
            raw_outline = json.loads(raw_data)
            outline = raw_outline.get("outline")
            if outline:
                questions = []
                def make_outline_question(data: dict, parent: "GS_Outline_Question"):
                    q = GS_Outline_Question(
                        self, 
                        question_id=data.get("id"),
                        crop_rect_list=[GS_Crop_info(**data.get("crop_rect_list", [])[0])],
                        title=data.get("title"),
                        weight=data.get("weight"),
                        
                    )
                    children = data.get("children")
                    if children:
                        for child in children:
                            c = make_outline_question(child, q)
                            q.add_child(c)
                    return q
                for question in outline:
                    questions.append(make_outline_question(question, None))
                id_regs = raw_outline.get("assignment", {}).get("id_regions", {})
                return GS_Outline(
                    GS_Crop_info(**id_regs.get("name", {})),
                    GS_Crop_info(**id_regs.get("sid", {})),
                    questions
                )
            

    def update_outline(self, outline: "GS_Outline") -> "GS_Outline":

        if self.client.edit_outline(self.course_id, self.assignment_id, outline.json()):
            return self.get_outline()
    
    def get_questions(self, raw_outline_data: str=None) -> ["GS_Question"]:
        if not raw_outline_data:
            raw_outline_data = self.client.get_assignment_outline(self.course_id, self.assignment_id)
        if raw_outline_data:
            raw_outline = json.loads(raw_outline_data)
            outline = raw_outline.get("outline")
            if outline:
                questions = []
                def make_question(data: dict, parent: "GS_Question"):
                    q = GS_Question(
                        self, 
                        question_id=data.get("id"),
                        parent=parent,
                        q_type=data.get("type"),
                        title=data.get("title"),
                        weight=data.get("weight"),
                        index=data.get("index")
                    )
                    children = data.get("children")
                    if children:
                        for child in children:
                            c = make_question(child, q)
                            q.add_child(c)
                    return q
                for question in outline:
                    questions.append(make_question(question, None))
                return questions

    def get_rubrics(self) -> dict:
        rubrics_data = self.client.grading_get_rubrics(self.course_id)
        assignments = rubrics_data.get("assignments")
        if assignments:
            for assignment in assignments:
                if str(assignment.get("id")) == str(self.assignment_id):
                    return assignment

class GS_Outline:
    def __init__(self, name_id_region: "GS_Crop_info", sid_region: "GS_Crop_info", question_data: ["GS_Outline_Question"]):
        self.name_id_region = name_id_region
        self.sid_region = sid_region
        self.question_data = question_data
        self.data = None # Extra variable for other programs to use

    def json(self):
        return {
            "assignment": {
                "identification_regions": {
                    "name": self.name_id_region.json(),
                    "sid": self.sid_region.json(),
                },
            },
            "question_data": [q.json() for q in self.question_data],
        }

    def get_question_number(self, question: "GS_Outline_Question", question_list: ["GS_Outline_Question"]=None, starting_index: str=""):
        count = 1
        if question_list is None:
            question_list = self.question_data
        for q in question_list:
            if q == question:
                return starting_index + str(count)
            if q.children:
                self.get_question_number(question, question_list=q.children, starting_index=f"{starting_index}{count}.")
        raise ValueError(f"Question {question} is not in this outline!")

    def questions_iterator(self):
        qnum = 1
        for question in self.question_data:
            yield from question.question_iterator(str(qnum))
            qnum += 1

class GS_Crop_info:
    def __init__(self, page_number: int, x1: int, y1: int, x2: int, y2: int):
        if not 0.0 <= x1 <= 100.0:
            raise ValueError(f"x1 must be between 0-100. Got: {x1}")
        if not 0.0 <= y1 <= 100.0:
            raise ValueError(f"y1 must be between 0-100. Got: {y1}")
        if not 0.0 <= x2 <= 100.0:
            raise ValueError(f"x2 must be between 0-100. Got: {x2}")
        if not 0.0 <= y2 <= 100.0:
            raise ValueError(f"y2 must be between 0-100. Got: {y2}")

        self.x1 = round(x1, 1)
        self.y1 = round(y1, 1)
        self.x2 = round(x2, 1)
        self.y2 = round(y2, 1)
        self.page_number = page_number
        self.data = None # Extra variable for other programs to use

    def json(self):
        return {
            "x1": self.x1,
            "x2": self.x2,
            "y1": self.y1,
            "y2": self.y2,
            "page_number": self.page_number
        }
        

class GS_Outline_Question:
    def __init__(self, assignment_grader: GS_assignment_Grader, question_id: str, crop_rect_list: [GS_Crop_info], children: ["GS_Outline_Question"]=None, title: str="", weight: int=1.0):
        self.assignment_grader = assignment_grader
        self.question_id = question_id
        if children is None:
            children = []
        self.children = children
        self.crop_rect_list = crop_rect_list
        self.title = title
        self.weight = weight
        self.data = None # Extra variable for other programs to use

    def json(self):
        data = {
            "crop_rect_list": [l.json() for l in self.crop_rect_list],
            "title": self.title,
            "weight": self.get_weight(),
        }
        if self.children:
            data["children"] = [child.json() for child in self.children]
        if self.question_id:
            data["id"] = self.question_id
        return data

    def get_gs_question(self) -> "GS_Question":
        q = GS_Question(self.assignment_grader, self.question_id, title=self.title, weight=self.weight)
        q.data = self.data
        return q

    def add_child(self, child: "GS_Outline_Question"):
        self.children.append(child)

    def question_iterator(self, qid: str):
        if self.children:
            cid = 1
            for child in self.children:
                yield from child.question_iterator(f"{qid}.{cid}")
                cid += 1
        else:
            yield (qid, self)

    def get_weight(self):
        if not self.children:
            return self.weight
        else:
            return sum([q.get_weight() for q in self.children])

class GS_Question:
    def __init__(self, assignment_grader: GS_assignment_Grader, question_id: str, parent: "GS_Question"=None, q_type: str=None, title: str=None, weight: str=None, index: str=None):
        self.assignment_grader = assignment_grader
        self.question_id = question_id
        self.parent = parent
        self.children = []
        self.q_type = q_type
        self.title = title
        self.weight = weight
        self.index = index
        self.data = None # Extra variable for other programs to use
    
    def set_children(self, children: ["GS_Question"]):
        self.children = children

    def add_child(self, child: "GS_Question"):
        self.children.append(child)

    def get_children(self):
        return self.children

    def set_group_type(self, group_type: GroupTypes):
        if self.question_id is None:
            return
        if isinstance(group_type, GroupTypes):
            group_type = group_type.value
        return self.assignment_grader.client.grouping_set_answer_type(self.assignment_grader.course_id, self.question_id, group_type)

    def is_grouping_ready(self):
        data = self.get_question_info()
        return data.get("status") == "ready"

    def get_groups(self):
        """
        A group has fields: id, question_id, question_type, position, internal_title, title, created_at, updated_at, hidden
        """
        data = self.get_question_info()
        return data.get("groups")

    def get_question_info(self):
        if self.question_id is None:
            return
        return self.assignment_grader.client.grouping_get_answer_groups(self.assignment_grader.course_id, self.question_id)

    def add_group(self, title: str) -> int:
        """
        Returns id of the group
        """
        res = self.assignment_grader.client.grading_create_group(self.assignment_grader.course_id, self.question_id, title)
        if res:
            return res.get("id")

    def group_submissions(self, group_id: int, submission_ids = [int]) -> bool:
        return self.assignment_grader.client.grading_add_to_group(self.assignment_grader.course_id, self.question_id, group_id, submission_ids)

    def get_rubric(self, assignment_rubrics_data: dict=None) -> dict:
        if assignment_rubrics_data is None:
            assignment_rubrics_data = self.assignment_grader.get_rubrics()

        if assignment_rubrics_data:
            for question in assignment_rubrics_data.get("questions", []):
                if question.get("id") == self.question_id:
                    return question

    def add_rubric_item(self, description: str, weight: float, get_res: bool=False) -> str:
        """
        Returns the id of the rubric item added if it succeeded
        """
        res = self.assignment_grader.client.add_rubric_item(self.assignment_grader.course_id, self.question_id, description, weight)
        if res:
            res = json.loads(res)
            if get_res:
                return res
            return res.get("id")

    def update_rubric_item(self, item_id: str, description: str=None, weight: float=None):
        res = self.assignment_grader.client.update_rubric_item(self.assignment_grader.course_id, self.question_id, item_id, description, weight)
        if res:
            return json.loads(res)

    def update_rubric_items(self, data: dict) -> bool:
        """ (can modify position, weight and description)
        E.g: {"rubric_items":{"16631449":{"position":1, "description": "MIDDLE"},"16631451":{"position":0, "weight": 42},"16969667":{"position":2, "description": "BOTT", "weight": 24}},"rubric_item_groups":{}}
        """
        return self.assignment_grader.client.update_rubric_items(self.assignment_grader.course_id, self.question_id, data)

    def delete_rubric_item(self, item_id: str) -> bool:
        return self.assignment_grader.client.delete_rubric_item(self.assignment_grader.course_id, self.question_id, item_id)
    
    def grade(self, submission_id: str, data: dict, save_group: bool=False) -> bool:
        """
        E.g.: {"rubric_items":{"16631449":{"score":"true"},"16631451":{"score":"true"},"16969667":{"score":"false"}},"question_submission_evaluation":{"points":"2.0","comments":null}}
        """
        return self.assignment_grader.client.grading_save(self.assignment_grader.course_id, self.question_id, submission_id, data, save_group)

    def get_submission_grader(self, submission_id: str=None) -> dict:
        if submission_id is None:
            submission_id = self.assignment_grader.client.grading_grade_first_ungraded_or_first(self.assignment_grader.course_id, self.question_id)
        if submission_id:
            return self.assignment_grader.client.grading_get_submission_grader(self.assignment_grader.course_id, self.question_id, submission_id)

class RubricItem:
    def __init__(self, id: int = None, description: str=None, weight: float=None, group_id: int=None, position: int=None):
        mod_locals = locals()
        mod_locals.pop("self", None)
        self.update(**mod_locals)
    
    def update(self, id: int = None, description: str=None, weight: float=None, group_id: int=None, position: int=None, **kwargs):
        self.item_id = id
        self.description = description
        self.weight = weight
        self.group_id = group_id
        self.position = position

    def rubric_item_selected_json(self, selected: bool) -> dict:
        if self.item_id is None:
            return
        return {
            self.item_id: {
                "score": selected
            }
        }


class QuestionRubric:
    def __init__(self, question: GS_Question):
        self.question = question
        self.rubric_items: RubricItem = []
        # TODO: This does not support grouped rubrics
        raw_rubric_items = question.get_rubric()
        if raw_rubric_items:
            for item in raw_rubric_items.get("rubric_items", []):
                self.rubric_items.append(RubricItem(**item))

    def add_rubric_item(self, rubric_item: RubricItem) -> bool:
        self.rubric_items.append(rubric_item)
        rubric_item.item_id = self.question.add_rubric_item(rubric_item.description, rubric_item.weight)
        return rubric_item.item_id is not None

    def delete_rubric_item(self, rubric_item: RubricItem) -> bool:
        if rubric_item in self.rubric_items:
            if self.question.delete_rubric_item(rubric_item.item_id):
                self.rubric_items.remove(rubric_item)
                return True
            else:
                return False
    
    def delete_existing_rubric(self) -> bool:
        for item in self.rubric_items:
            self.delete_rubric_item(item)
        return len(self.rubric_items) == 0
    
    def update_rubric_item(self, rubric_item: RubricItem, description: str=None, weight: float=None) -> bool:
        if description is None and weight is None:
            return True
        if description is None:
            description = rubric_item.description
        if weight is None:
            weight = rubric_item.weight
        res = self.question.update_rubric_item(rubric_item.item_id, description=description, weight=weight)
        if res:
            rubric_item.update(**res)
            return True
        return False

    def grade(self, submission_id: int, selection_list, save_group: bool=False) -> bool:
        """
        Takes in the submission id to grade, a selection list which is a list of just true and false
        in the same order as the internal rubric or a dictionary mapping rubric item to bool (if it is selected.)
        selection_list: Union[{RubricItem:bool}, [bool]]
        """
        rubric_items = {}
        data = {
            "rubric_items": rubric_items,
            "question_submission_evaluation": {
                "points": None,
                "comments": None
            }
        }

        if isinstance(selection_list, dict):
            for item, selected in selection_list.items():
                rubric_items[item.item_id] = {"score": json.dumps(selected)}

        elif isinstance(selection_list, list):
            if len(selection_list) != len(self.rubric_items):
                raise ValueError("The selection list must match the number of items in the rubric!")
            for i, v in enumerate(selection_list):
                rubric_items[self.rubric_items[i].item_id] = {"score": json.dumps(v)}
        else:
            raise ValueError(f"{type(selection_list)} not supported")

        return self.question.grade(submission_id, data, save_group=save_group)

    def __len__(self):
        return len(self.rubric_items)

    def get_rubric_items(self):
        return self.rubric_items