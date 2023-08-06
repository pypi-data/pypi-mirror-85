import requests
import getpass
from bs4 import BeautifulSoup
import bs4
import re
from .cdata import GS_CDATA_decoder
from .autograder import GS_autograder
from .online_assignment import GS_online_assignment
from .assignment_grader import GS_assignment_Grader
import json

class GradescopeClient:
    base_url = "https://gradescope.com"
    login_path = "/login"
    def __init__(self, logout_on_del: bool=False, logout_on_with: bool=False, user_agent: str="fullGSapi"):
        self.session = requests.Session()
        headers={"User-Agent":user_agent}
        # headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"}
        self.session.headers.update(headers)
        self.logged_in = False
        self.last_res = None
        self.last_soup = None
        self.logout_on_del = logout_on_del
        self.logout_on_with = logout_on_with
    
    def __del__(self):
        try:
            if self.logged_in and self.logout_on_del:
                self.logout()
        except Exception as e:
            print(f"Failed to logout of Gradescope! {e}")

    def __enter__(self):
        if not self.logged_in:
            self.prompt_login()
        if not self.logged_in:
            raise ValueError("You must be logged in to use this client!")
        return self

    def __exit__(self, type, value, traceback):
        if self.logout_on_with and self.logged_in:
            self.logout()

    def is_logged_in(self):
        return self.logged_in

    def verify_logged_in(self):
        if not self.logged_in:
            return False
        # url = self.base_url + "/account"
        # self.last_res = self.session.get(url)
        # return self.last_res.ok
        url = self.base_url + "/login"
        self.last_res = res = self.session.get(url)
        # If you are logged in and visit the login page, it returns a 401 error
        # and will return content b'{"warning":"You must be logged out to access this page."}'
        return res.status_code == 401

    def submit_form(self, url, ref_url, data=None, files=None, header_token=None, json=None):
        headers={
            "Host": "www.gradescope.com",
            "Origin": "https://www.gradescope.com",
            "Referer": ref_url
        }
        if header_token is not None:
            headers["X-CSRF-Token"] = header_token
        self.last_res = res = self.session.post(url, data=data, json=json, files=files, headers = headers)
        return res

    def get_token(self, url, action=None, meta=None):
        self.last_res = res = self.session.get(url)
        self.last_soup = soup = BeautifulSoup(res.content, "html.parser")
        form = None
        if action:
            form = soup.find("form", {"action":action})
        elif meta:
            return soup.find("meta", {"name": meta})['content']
        else:
            form = soup.find("form")
        return form.find("input", {"name":"authenticity_token"})['value']

    def log_in(self, email, password):
        url = self.base_url + self.login_path
        token = self.get_token(url)
        payload = {
            "utf8": "✓",
            "authenticity_token": token,
            "session[email]": email,
            "session[password]": password,
            "session[remember_me]": 1,
            "commit": "Log In",
            "session[remember_me_sso]": 0,
        }
        self.last_res = res = self.submit_form(url, url, data=payload)
        if res.ok:
            self.logged_in = True
            return True
        return False
        
    def prompt_login(self):
        while not self.logged_in:
            email = input("Please provide the email address on your Gradescope account: ")
            password = getpass.getpass('Password: ')
            if not self.log_in(email, password):
                print("An error occurred when attempting to log you in, try again...")
            else:
                self.logged_in = True
    
    def logout(self):
        print("Logging out")
        if not self.logged_in:
            print("You must be logged in!")
            return
        base_url = f"https://www.gradescope.com"
        url = base_url + "/logout"
        ref_url = base_url + "/account"
        self.last_res = res = self.session.get(url, headers={"Referer": ref_url})
        if res.ok:
            self.logged_in = False
            return True
        return False

    def download_scores(self, class_id: str, assignment_id: str, filetype: str="csv") -> bytes:
        if not self.logged_in:
            print("You must be logged in to download grades!")
            return False
        self.last_res = res = self.session.get(f"https://www.gradescope.com/courses/{class_id}/assignments/{assignment_id}/scores.{filetype}")
        if not res or not res.ok:
            print(f"Failed to get a response from gradescope! Got: {res}")
            return False
        return res.content
    
    def regrade_submission(self, class_id: str, assignment_id: str, submission_id: str) -> bool:
        if not self.logged_in:
            print("You must be logged in to regrade a submission!")
            return
        base_url = f"https://www.gradescope.com"
        location_url = f"/courses/{class_id}/assignments/{assignment_id}/submissions/{submission_id}"
        url = base_url + location_url
        regrade_url = f"{url}/regrade"
        token = self.get_token(url, action=location_url + "/regrade")
        payload = {
            "authenticity_token": token
        }
        self.last_res = res = self.submit_form(regrade_url, url, data=payload)
        return res.ok

    def regrade_all(self, class_id: str, assignment_id: str) -> bool:
        if not self.logged_in:
            print("You must be logged in to regrade all submissions!")
            return
        base_url = f"https://www.gradescope.com"
        location_url = f"/courses/{class_id}/assignments/{assignment_id}/submissions"
        url = base_url + location_url + "/regrade"
        token = self.get_token(url, meta="csrf-token")
        payload = {
            "authenticity_token": token
        }
        self.last_res = res = self.submit_form(url, location_url, data=payload)
        return res.ok

    def rebuild_autograder(self, class_id: str, assignment_id: str, file_name: str) -> bool:
        if not self.logged_in:
            print("You must be logged in to rebuild an autograder!")
            return
        base_url = f"https://www.gradescope.com"
        location_url = f"/courses/{class_id}/assignments/{assignment_id}"
        referer_url = base_url + location_url + "/configure_autograder"
        url = base_url + location_url
        token = self.get_token(referer_url, meta="csrf-token")
        ain = self.last_soup.find(id="assignment_image_name")
        image_name = ain.get('value', "")
        payload = {
                "utf8": "✓",
                "_method": "patch",
                "authenticity_token": token,
                "configuration": "zip",
                # "autograder_zip": (file_name, open(file_name, 'rb'), 'text/plain'),
                "assignment[image_name]": image_name,
            }
        files = {
            "autograder_zip": (file_name, open(file_name, 'rb'))
        }
        self.last_res = res = self.submit_form(url, referer_url, data=payload, files=files)
        return res.ok

    def set_manual_ag_config(self, class_id: str, assignment_id: str, image: str) -> bool:
        if not self.logged_in:
            print("You must be logged in to rebuild an autograder!")
            return
        base_url = f"https://www.gradescope.com"
        location_url = f"/courses/{class_id}/assignments/{assignment_id}"
        referer_url = base_url + location_url + "/configure_autograder"
        url = base_url + location_url
        token = self.get_token(referer_url, meta="csrf-token")
        payload = {
                "utf8": "✓",
                "_method": "patch",
                "authenticity_token": token,
                "configuration": "manual",
                # "autograder_zip": (file_name, open(file_name, 'rb'), 'text/plain'),
                "assignment[image_name]": image,
            }
        files = {
            "autograder_zip": ("", "")
        }
        self.last_res = res = self.submit_form(url, referer_url, data=payload, files=files)
        return res.ok
        
    def ag_building_data(self, class_id: str, assignment_id: str):
        if not self.logged_in:
            print("You must be logged in to check the autograder image status!")
            return
        base_url = f"https://www.gradescope.com"
        location_url = f"/courses/{class_id}/assignments/{assignment_id}"
        referer_url = base_url + location_url + "/configure_autograder"
        url = base_url + location_url
        self.last_res = res = self.session.get(referer_url)
        self.last_soup = soup = BeautifulSoup(res.content, "html.parser")
        # cdata = self.last_soup.find(text=re.compile("CDATA"))
        # matches = re.search(r"\"status\"\s*:\s*\"(.*?)\"", cdata)
        # return matches[1]
        cdata = GS_CDATA_decoder(soup=soup)
        return cdata.get_gon()

    def get_submission_data(self, class_id: str, assignment_id: str, submission_id: str):
        if not self.logged_in:
            print("You must be logged in to get submission data!")
            return
        base_url = f"https://www.gradescope.com"
        location_url = f"/courses/{class_id}/assignments/{assignment_id}/submissions/{submission_id}"
        url = base_url + location_url
        self.last_res = res = self.session.get(url)
        if res.ok:
            return res.content
    
    def get_autograder(self, class_id: str, assignment_id: str):
        if not self.logged_in:
            print("You must be logged in to get an autograders data!")
            return
        return GS_autograder(self, class_id, assignment_id)
    
    def get_docker_image(self, class_id: str, assignment_id: str, docker_image_id: str) -> dict:
        if not self.logged_in:
            print("You must be logged in to get an autograders data!")
            return
        base_url = f"https://www.gradescope.com"
        location_url = f"/courses/{class_id}/assignments/{assignment_id}/docker_images/{docker_image_id}.json"
        url = base_url + location_url
        self.last_res = res = self.session.get(url)
        if res.ok:
            return json.loads(res.content)
        return {}

    def update_online_assignment(self, class_id: str, assignment_id: str, outline: str) -> bool:
        data = {
            "outline": outline
        }
        return self.edit_outline(class_id, assignment_id, data)

    def get_online_assignment_outline(self, class_id: str, assignment_id: str) -> str:
        if not self.logged_in:
            print("You must be logged in to get an online assignment!")
            return
        base_url = f"https://www.gradescope.com"
        location_url = f"/courses/{class_id}/assignments/{assignment_id}/outline/edit"
        url = base_url + location_url
        self.last_res = res = self.session.get(url)
        if not res or not res.ok:
            print(f"Failed to get a response from gradescope! Got: {res}")
            return ""
        self.last_soup = soup = BeautifulSoup(res.content, "html.parser")
        editors = soup.find_all("div", {"data-react-class": "AssignmentEditor"})
        if len(editors) == 0:
            print(f"Could not find online submission data!")
            return ""
        return editors[0]['data-react-props']

    def get_online_assignment_new_submission(self, class_id: str, assignment_id: str) -> str:
        if not self.logged_in:
            print("You must be logged in to get an online assignment!")
            return
        base_url = f"https://www.gradescope.com"
        location_url = f"/courses/{class_id}/assignments/{assignment_id}/submissions/new"
        url = base_url + location_url
        self.last_res = res = self.session.get(url)
        if not res or not res.ok:
            print(f"Failed to get a response from gradescope! Got: {res}")
            return ""
        self.last_soup = soup = BeautifulSoup(res.content, "html.parser")
        editors = soup.find_all("div", {"data-react-class": "OnlineAssignmentSubmitter"})
        if len(editors) == 0:
            print(f"Could not find online submission data!")
            return ""
        return editors[0]['data-react-props']

    def submit_online_assignment(self, class_id: str, assignment_id: str, owner_id: str, questions: str) -> bool:
        if not self.logged_in:
            print("You must be logged in to submit an online assignment!")
            return
        base_url = f"https://www.gradescope.com"
        location_url = f"/courses/{class_id}/assignments/{assignment_id}/submissions"
        url = base_url + location_url
        ref_url = url + "/new"
        token = self.get_token(ref_url, meta="csrf-token")
        data = {
            "questions": questions,
            "owner_id": owner_id
        }
        return self.submit_form(url, ref_url, data=data, header_token=token).ok

    def get_online_assignment(self, class_id: str, assignment_id: str) -> GS_online_assignment:
        return GS_online_assignment(self, class_id, assignment_id)

    def get_assignment_outline(self, class_id: str, assignment_id: str) -> str:
        if not self.logged_in:
            print("You must be logged in to get an online assignment!")
            return
        base_url = f"https://www.gradescope.com"
        location_url = f"/courses/{class_id}/assignments/{assignment_id}/outline/edit"
        url = base_url + location_url
        self.last_res = res = self.session.get(url)
        if not res or not res.ok:
            print(f"Failed to get a response from gradescope! Got: {res}")
            return ""
        self.last_soup = soup = BeautifulSoup(res.content, "html.parser")
        editors = soup.find_all("div", {"data-react-class": "AssignmentOutline"})
        if len(editors) == 0:
            print(f"Could not find online submission data!")
            return ""
        return editors[0]['data-react-props']

    def add_rubric_item(self, class_id: str, question_id: str, description: str, weight: float) -> dict:
        if not self.logged_in:
            print("You must be logged in!")
            return
        base_url = f"https://www.gradescope.com"
        location_url = f"/courses/{class_id}/questions/{question_id}/rubric_items"
        ref_url = base_url + location_url
        headers={
            "Host": "www.gradescope.com",
            "Origin": "https://www.gradescope.com",
            "Referer": ref_url,
            "X-CSRF-Token": self.get_token(ref_url, meta="csrf-token")
        }
        payload = {
            "rubric_item": {
                "description": description, 
                "weight": str(weight),
                }
        }
        self.last_res = res = self.session.post(ref_url, headers=headers, json=payload)
        if res.ok:
            return res.content
    
    def update_rubric_item(self, class_id: str, question_id: str, item_id: str, description: str=None, weight: float=None) -> dict:
        if not self.logged_in:
            print("You must be logged in!")
            return
        if description is None and weight is None:
            raise ValueError("You must update at least one item!")
        base_url = f"https://www.gradescope.com"
        location_url = f"/courses/{class_id}/questions/{question_id}/rubric_items"
        ref_url = base_url + location_url + "/grade"
        url = base_url + location_url + f"/{item_id}"
        headers={
            "Host": "www.gradescope.com",
            "Origin": "https://www.gradescope.com",
            "Referer": ref_url,
            "X-CSRF-Token": self.get_token(ref_url, meta="csrf-token")
        }
        payload = {
            "id": question_id
        }
        if description is not None:
            payload["description"] = description
        if weight is not None:
            payload["weight"] = weight
        self.last_res = res = self.session.put(url, headers=headers, json=payload)
        if res.ok:
            return res.content

    def delete_rubric_item(self, class_id: str, question_id: str, item_id: str) -> bool:
        if not self.logged_in:
            print("You must be logged in!")
            return
        base_url = f"https://www.gradescope.com"
        location_url = f"/courses/{class_id}/questions/{question_id}/rubric_items"
        ref_url = base_url + location_url + "/grade"
        url = base_url + location_url + f"/{item_id}"
        headers={
            "Host": "www.gradescope.com",
            "Origin": "https://www.gradescope.com",
            "Referer": ref_url,
            "X-CSRF-Token": self.get_token(ref_url, meta="csrf-token")
        }
        self.last_res = res = self.session.delete(url, headers=headers)
        return res.ok

    def get_grade_submission_data(self, class_id: str, question_id: str, submission_id: str) -> dict:
        if not self.logged_in:
            print("You must be logged in!")
            return
        base_url = f"https://www.gradescope.com"
        location_url = f"/courses/{class_id}/questions/{question_id}/submissions/{submission_id}"
        url = base_url + location_url
        ref_url = url + "/grade"
        headers={
            "Host": "www.gradescope.com",
            "Origin": "https://www.gradescope.com",
            "Referer": ref_url,
            "X-CSRF-Token": self.get_token(ref_url, meta="csrf-token")
        }
        self.last_res = res = self.session.get(url, headers=headers)
        if res.ok:
            return json.loads(res.content)

    def update_rubric_items(self, class_id: str, question_id: str, data: dict) -> bool:
        """ (can modify position, weight and description)
        E.g: {"rubric_items":{"16631449":{"position":1, "description": "MIDDLE"},"16631451":{"position":0, "weight": 42},"16969667":{"position":2, "description": "BOTT", "weight": 24}},"rubric_item_groups":{}}
        """
        if not self.logged_in:
            print("You must be logged in!")
            return
        base_url = f"https://www.gradescope.com"
        location_url = f"/courses/{class_id}/questions/{question_id}/rubric/update_entries"
        ref_url = base_url + location_url
        url = ref_url
        headers={
            "Host": "www.gradescope.com",
            "Origin": "https://www.gradescope.com",
            "Referer": ref_url,
            "X-CSRF-Token": self.get_token(ref_url, meta="csrf-token")
        }
        self.last_res = res = self.session.patch(url, headers=headers, json=data)
        return res.ok

    def grading_save(self, class_id: str, question_id: str, submission_id: str, data: dict, save_group: bool=False):
        """
        E.g.: {"rubric_items":{"16631449":{"score":"true"},"16631451":{"score":"true"},"16969667":{"score":"false"}},"question_submission_evaluation":{"points":"2.0","comments":null}}
        """
        if not self.logged_in:
            print("You must be logged in!")
            return
        base_url = f"https://www.gradescope.com"
        location_url = f"/courses/{class_id}/questions/{question_id}/submissions/{submission_id}"
        ref_url = base_url + location_url
        url = ref_url + ("/save_many_grades" if save_group else "/save_grade")
        ref_url += "/grade"
        headers={
            "Host": "www.gradescope.com",
            "Origin": "https://www.gradescope.com",
            "Referer": ref_url,
            "X-CSRF-Token": self.get_token(ref_url, meta="csrf-token")
        }
        self.last_res = res = self.session.post(url, headers=headers, json=data)
        return res.ok

    def publish_grades(self, class_id: str, assignment_id: str, publish: bool=True) -> bool:
        if not self.logged_in:
            print("You must be logged in!")
            return
        base_url = f"https://www.gradescope.com"
        location_url = f"/courses/{class_id}/assignments/{assignment_id}"
        url = base_url + location_url
        ref_url = url + "/review_grades"
        token = self.get_token(ref_url, meta="csrf-token")
        payload = {
            "_method": "put",
            "authenticity_token": token,
            "assignment[published]": publish
        }
        self.last_res = res = self.submit_form(url, location_url, data=payload)
        return res.ok

    def edit_outline(self, class_id: str, assignment_id: str, data: dict) -> bool:
        """
        E.g.
        {
        "assignment": {
            "identification_regions": {
            "name": {
                "x1": 2.3,
                "x2": 19,
                "y1": 11,
                "y2": 15.7,
                "page_number": 1
            },
            "sid": {
                "x1": 2.6,
                "x2": 18.9,
                "y1": 16.9,
                "y2": 22.6,
                "page_number": 1
            }
            }
        },
        "question_data": [
            {
            "title": "",
            "weight": 2,
            "crop_rect_list": [
                {
                "x1": 3.7,
                "x2": 26.6,
                "y1": 16.7,
                "y2": 22.7,
                "page_number": 2
                }
            ],
            "children": [
                {
                "title": "",
                "weight": 1,
                "crop_rect_list": [
                    {
                    "x1": 3.7,
                    "x2": 26.6,
                    "y1": 16.7,
                    "y2": 22.7,
                    "page_number": 2
                    }
                ]
                },
                {
                "title": "",
                "weight": 1,
                "crop_rect_list": [
                    {
                    "x1": 2.4,
                    "x2": 25.3,
                    "y1": 9,
                    "y2": 15,
                    "page_number": 3
                    }
                ]
                }
            ]
            },
            {
            "title": "",
            "weight": 1,
            "crop_rect_list": [
                {
                "x1": 3.9,
                "x2": 26.8,
                "y1": 37.7,
                "y2": 45.9,
                "page_number": 4
                }
            ]
            }
        ]
        }
        """
        if not self.logged_in:
            print("You must be logged in!")
            return
        base_url = f"https://www.gradescope.com"
        location_url = f"/courses/{class_id}/assignments/{assignment_id}/outline/"
        url = base_url + location_url
        ref_url = url + "edit"
        headers={
            "Host": "www.gradescope.com",
            "Origin": "https://www.gradescope.com",
            "Referer": ref_url,
            "X-CSRF-Token": self.get_token(ref_url, meta="csrf-token")
        }
        self.last_res = res = self.session.patch(url, json=data, headers = headers)
        return res

    def grouping_set_answer_type(self, class_id: str, question_id: str, group_type: str) -> bool:
        """
        Group Types:
        complex - Group unanswered
        non_grouped - Not Grouped
        mc - multiple choice
        math - math fill in the blank
        words - Text fill in the blank
        """
        if not self.logged_in:
            print("You must be logged in!")
            return
        base_url = f"https://www.gradescope.com"
        location_url = f"/courses/{class_id}/questions/{question_id}"
        url = base_url + location_url
        ref_url = url + "/answer_groups/"
        headers={
            "Host": "www.gradescope.com",
            "Origin": "https://www.gradescope.com",
            "Referer": ref_url,
            "X-CSRF-Token": self.get_token(ref_url, meta="csrf-token")
        }
        data = {
            "question": {
                "assisted_grading_type": group_type,
            },
        }
        self.last_res = res = self.session.patch(url, json=data, headers = headers)
        return res
    
    def old_grouping_get_answer_groups(self, class_id: str, question_id: str) -> dict:
        if not self.logged_in:
            print("You must be logged in!")
            return
        base_url = f"https://www.gradescope.com"
        location_url = f"/courses/{class_id}/questions/{question_id}/answer_groups"
        url = base_url + location_url
        self.last_res = res = self.session.get(url)
        if not res or not res.ok:
            print(f"Failed to get a response from gradescope! Got: {res}")
            return ""
        self.last_soup = soup = BeautifulSoup(res.content, "html.parser")
        editors = soup.find_all("div", {"data-react-class": "AnswerGrouper"})
        if len(editors) == 0:
            print(f"Could not find data!")
            return ""
        return json.loads(editors[0]['data-react-props']).get("groups")

    def grouping_get_answer_groups(self, class_id: str, question_id: str) -> dict:
        if not self.logged_in:
            print("You must be logged in!")
            return
        base_url = f"https://www.gradescope.com"
        location_url = f"/courses/{class_id}/questions/{question_id}/answer_groups.json"
        url = base_url + location_url
        self.last_res = res = self.session.get(url)
        if not res or not res.ok:
            print(f"Failed to get a response from gradescope! Got: {res}")
            return ""
        return json.loads(res.content)

    def grading_create_group(self, class_id: str, question_id: str, title: str, internal_title: str=None) -> bool:
        if not self.logged_in:
            print("You must be logged in!")
            return
        base_url = f"https://www.gradescope.com"
        location_url = f"/courses/{class_id}/questions/{question_id}/answer_groups"
        url = base_url + location_url
        ref_url = url + "/ungrouped"
        token = self.get_token(ref_url, meta="csrf-token")
        payload = {
            "internal_title": internal_title,
            "title": title,
        }
        self.last_res = res = self.submit_form(url, location_url, json=payload, header_token=token)
        if res.ok:
            return json.loads(res.content)

    def grading_add_to_group(self, class_id: str, question_id: str, group_id: str, submissions_ids: [int]) -> bool:
        """
        Group ID is the id of the group you wanna add the submissions to.
        If you want to unset a submission, just set answer groups to None.
        """
        if not self.logged_in:
            print("You must be logged in!")
            return
        base_url = f"https://www.gradescope.com"
        location_url = f"/courses/{class_id}/questions/{question_id}"
        url = base_url + location_url + "/answer_group_memberships/many"
        ref_url = base_url + location_url + "/answer_groups/ungrouped"
        token = self.get_token(ref_url, meta="csrf-token")
        payload = {
            "answer_group_id": group_id,
            "submission_ids": submissions_ids,
        }
        self.last_res = res = self.submit_form(url, location_url, json=payload, header_token=token)
        # if self.last_res.ok:
        #     return json.loads(self.last_res.content)
        return res.ok

    def export_evaluations(self, class_id: str, assignment_id: str) -> bytes:
        if not self.logged_in:
            print("You must be logged in to download grades!")
            return False
        self.last_res = res = self.session.get(f"https://www.gradescope.com/courses/{class_id}/assignments/{assignment_id}/export_evaluations")
        if not res or not res.ok:
            print(f"Failed to get a response from gradescope! Got: {res}")
            return False
        return res.content
    
    def get_assignment_grader(self, class_id: str, assignment_id: str) -> GS_assignment_Grader:
        return GS_assignment_Grader(self, class_id, assignment_id)

    def old_grading_get_submission_grader(self, class_id: str, question_id: str, submission_id: str) -> str:
        if not self.logged_in:
            print("You must be logged in!")
            return
        base_url = f"https://www.gradescope.com"
        location_url = f"/courses/{class_id}/questions/{question_id}/submissions/{submission_id}/grade"
        url = base_url + location_url
        self.last_res = res = self.session.get(url)
        if not res or not res.ok:
            print(f"Failed to get a response from gradescope! Got: {res}")
            return ""
        self.last_soup = soup = BeautifulSoup(res.content, "html.parser")
        editors = soup.find_all("div", {"data-react-class": "SubmissionGrader"})
        if len(editors) == 0:
            print(f"Could not find online submission data!")
            return ""
        return editors[0]['data-react-props']

    def grading_get_submission_grader(self, class_id: str, question_id: str, submission_id: str) -> str:
        if not self.logged_in:
            print("You must be logged in!")
            return
        base_url = f"https://www.gradescope.com"
        location_url = f"/courses/{class_id}/questions/{question_id}/submissions/{submission_id}/grade.json"
        url = base_url + location_url
        self.last_res = res = self.session.get(url)
        if not res or not res.ok:
            print(f"Failed to get a response from gradescope! Got: {res}")
            return ""
        return res.content

    def grading_grade_first_ungraded_or_first(self, class_id: str, question_id: str) -> str:
        """
        Returns the first ungraded submission id of the question.
        """
        if not self.logged_in:
            print("You must be logged in!")
            return
        base_url = f"https://www.gradescope.com"
        location_url = f"/courses/{class_id}/questions/{question_id}/submissions/grade_first_ungraded_or_first"
        url = base_url + location_url
        self.last_res = res = self.session.get(url, headers={"referer": f"https://www.gradescope.com/courses/{class_id}/questions/{question_id}/answer_groups/ungrouped"})
        if not res or not res.ok:
            print(f"Failed to get a response from gradescope! Got: {res}")
            return
        red_url = res.url
        reg_pat = r"https:\/\/www\.gradescope\.com\/courses\/[0-9]+\/questions\/[0-9]+\/submissions\/([0-9]+)\/grade"
        matches = re.match(reg_pat, red_url)
        if matches:
            return matches[1]

    def grading_get_rubrics(self, class_id: str) -> dict:
        if not self.logged_in:
            print("You must be logged in!")
            return
        base_url = f"https://www.gradescope.com"
        location_url = f"/courses/{class_id}"
        url = base_url + location_url + "/assignments/rubrics"
        self.last_res = res = self.session.get(url)
        if res.ok:
            return json.loads(res.content)

    def grouping_delete_answer_group(self, class_id: str, question_id: str, answer_group_id: str) -> bool:
        if not self.logged_in:
            print("You must be logged in!")
            return
        base_url = f"https://www.gradescope.com"
        location_url = f"/courses/{class_id}/questions/{question_id}/answer_groups"
        ref_url = base_url + location_url
        url = ref_url + f"/{answer_group_id}"
        headers={
            "Host": "www.gradescope.com",
            "Origin": "https://www.gradescope.com",
            "Referer": ref_url,
            "X-CSRF-Token": self.get_token(ref_url, meta="csrf-token")
        }
        self.last_res = res = self.session.delete(url, headers=headers)
        return res.ok

    def create_exam(self, class_id: str, title: str, template: str) -> str:
        """
        Returns the assignment id
        """
        if not self.logged_in:
            print("You must be logged in!")
            return
        url = self.base_url + f"/courses/{class_id}/assignments"
        token = self.get_token(url, meta="csrf-token")
        payload = {
            "authenticity_token": token,
            "assignment[title]": title,
            "assignment[student_submission]": "false",
            "utf8": "✓",
            "assignment[type]": "PDFAssignment",
            "assignment[bubble_sheet]": "false",
            "assignment[release_date_string]": "",
            "assignment[due_date_string]": "",
            "allow_late_submissions": "0",
            "assignment[submission_type]": "pdf",
            "assignment[group_submission]": "0",
            "assignment[template_visible_to_students]": "0",
            "commit": "Next",
        }
        files = {
            "template_pdf": (template, open(template, 'rb'), "application/pdf")
        }
        self.last_res = res = self.submit_form(url, url, data=payload, files=files)
        if res.ok:
            template_url = ""
            red_url = res.url
            reg_pat = r"https:\/\/www\.gradescope\.com\/courses/[0-9]+/assignments/([0-9]+)/outline/edit"
            matches = re.match(reg_pat, red_url)
            if matches:
                return matches[1]

    def create_programming_assignment(self, class_id: str, title: str, total_points: float, manual_grading: bool, student_submission: bool, release_date: str, due_date: str, allow_late_submissions: bool, group_submission: bool, leaderboard_enabled: bool, hard_due_date: str=None, group_size: int=None, leaderboard_max_entries: int=None) -> str:
        """
        Returns the assignment id

        authenticity_token: 5tk+AedAm6Yl++q926aaxetR5WcoSgYUNGLpqhTzESHB49XHxWmirEafcZdsXgl9H6pe7Ryk25auktrSrdjZsA==
        assignment[type]: ProgrammingAssignment
        assignment[title]: New Assignment
        assignment[total_points]: 23
        assignment[manual_grading]: 0
        assignment[student_submission]: true
        assignment[release_date_string]: Oct 13 2020 07:00 PM
        assignment[due_date_string]: Oct 17 2020 07:00 PM
        assignment[allow_late_submissions]: 0
        assignment[group_submission]: 0
        assignment[leaderboard_enabled]: 0
        ----
        authenticity_token: uphwsAOixw1dd5gKuO+oA7tFWSxMAETPgTlS7tqAdPmdopt2IYv+Bz4TAyAPFzu7T77ipnjumU0byWGWY6u8aA==
        assignment[type]: ProgrammingAssignment
        assignment[title]: New 2 Assignment
        assignment[total_points]: 100.1
        assignment[manual_grading]: 0
        assignment[manual_grading]: 1
        assignment[student_submission]: true
        assignment[release_date_string]: Oct 13 2020 07:00 PM
        assignment[due_date_string]: Oct 15 2020 07:00 PM
        assignment[allow_late_submissions]: 0
        assignment[allow_late_submissions]: 1
        assignment[hard_due_date_string]: Oct 16 2020 07:00 PM
        assignment[group_submission]: 0
        assignment[group_submission]: 1
        assignment[group_size]: 
        assignment[leaderboard_enabled]: 0
        assignment[leaderboard_enabled]: 1

        """
        if not self.logged_in:
            print("You must be logged in!")
            return
        url = self.base_url + f"/courses/{class_id}/assignments"
        token = self.get_token(url, meta="csrf-token")
        payload = {
            "authenticity_token": token,
            "assignment[type]": "ProgrammingAssignment",
            "assignment[title]": title,
            "assignment[total_points]": total_points,
            "assignment[manual_grading]": int(manual_grading),
            "assignment[student_submission]": student_submission,
            "assignment[release_date_string]": release_date,
            "assignment[due_date_string]": due_date,
            "assignment[allow_late_submissions]": int(allow_late_submissions),
            "assignment[group_submission]": int(group_submission),
            "assignment[leaderboard_enabled]": int(leaderboard_enabled)
        }
        if allow_late_submissions:
            payload["assignment[hard_due_date_string]"] = hard_due_date
        if group_submission:
            payload["assignment[group_size]"] = group_size
        if leaderboard_enabled:
            payload["assignment[leaderboard_max_entries]"] = leaderboard_max_entries

        self.last_res = res = self.submit_form(url, url, data=payload)
        if res.ok:
            red_url = res.url
            reg_pat = r"https:\/\/www\.gradescope\.com\/courses\/[0-9]+\/assignments\/([0-9]+)\/(?:configure_autograder|outline\/edit)"
            matches = re.match(reg_pat, red_url)
            if matches:
                return matches[1]

    def scrape_autograder_results(self, class_id: str, assignment_id: str, submission_id: str):
        """
        Returns a dictionary of test case information:
        {
            autograder_score,
            max_score,
            output,
            tests : [
                {
                    name,
                    score,
                    max_score,
                    output,
                    passed
                }
            ]
        }
        """
        if not self.logged_in:
            print("You must be logged in to check the autograder image status!")
            return
        base_url = f"https://www.gradescope.com"
        location_url = f"/courses/{class_id}/assignments/{assignment_id}/submissions/{submission_id}"
        url = base_url + location_url
        self.last_res = res = self.session.get(url)
        self.last_soup = soup = BeautifulSoup(res.content, "html.parser")
        header = soup.find_all("div", class_="testCase--header")
        body = soup.find_all("div", class_="testCase--body")
        tests = []
        total_points_string = soup.find_all("div", class_="submissionOutlineHeader--totalPoints")[0].text
        score, max_score = map(str.strip, total_points_string.split("/"))
        output = None
        output_div = soup.find_all("div", class_="autograderResults--topLevelOutput")
        if output_div:
            output = output_div[0].find("div").text
        r = {
            "tests": tests,
            "score": score,
            "max_score": max_score,
            "output": output
        }
        score_re = re.compile(r"\((\d+(?:.\d+))\s*\/\s*(\d+(?:.\d+))\)")
        for i, item in enumerate(header):
            data = item.find("a")
            if data: # Is test case
                name = data.attrs["name"]
                score = max_score = None
                score_match = re.findall(score_re, data.text)
                if score_match:
                    m = score_match[0]
                    score = float(m[0])
                    max_score = float(m[1])
                classes = item.parent.attrs["class"]
                if "testCase-passed" in classes:
                    passed = True
                elif "testCase-failed" in classes:
                    passed = False
                else:
                    passed = None
                tests.append({
                    "name": name,
                    "score": score,
                    "max_score": max_score,
                    "output": body[i].find("pre").text,
                    "passed": passed,
                })
            else: # Is hidden output
                tests.append({
                    "name": item.text,
                    "score": None,
                    "max_score": None,
                    "output": json.loads(body[i].find("div").attrs["data-react-props"])["children"],
                    "passed": None,
                })
        return r
        
    def start_export_submissions(self, class_id: str, assignment_id: str) -> int:
        if not self.logged_in:
            print("You must be logged in!")
            return
        base_url = f"https://www.gradescope.com/courses/{class_id}/assignments/{assignment_id}/"
        location_url = base_url + f"review_grades"
        url = base_url + "export"
        token = self.get_token(location_url, meta="csrf-token")
        payload = {
            "authenticity_token": token
        }
        self.last_res = res = self.submit_form(url, location_url, data=payload)
        if res.status_code == 200:
            return json.loads(res.content).get("generated_file_id")
        return None

    def check_gon_export_submissions_progress(self, class_id: str, assignment_id: str):
        if not self.logged_in:
            print("You must be logged in!")
            return
        base_url = f"https://www.gradescope.com/courses/{class_id}/assignments/{assignment_id}/"
        url = base_url + f"review_grades"
        self.last_res = res = self.session.get(url)
        self.last_soup = soup = BeautifulSoup(res.content, "html.parser")
        cdata = GS_CDATA_decoder(soup=soup)
        return cdata.get_gon().get("generated_file")
    
    def check_export_submissions_progress(self, class_id: str, generated_files_id: str):
        if not self.logged_in:
            print("You must be logged in!")
            return
        base_url = f"https://www.gradescope.com"
        location_url = f"/courses/{class_id}"
        url = base_url + location_url + f"/generated_files/{generated_files_id}.json"
        self.last_res = res = self.session.get(url)
        if res.ok:
            return json.loads(res.content)

    def download_export_submissions(self, class_id: str, generated_files_id: str):
        if not self.logged_in:
            print("You must be logged in!")
            return
        base_url = f"https://www.gradescope.com"
        location_url = f"/courses/{class_id}"
        url = base_url + location_url + f"/generated_files/{generated_files_id}.zip"
        self.last_res = res = self.session.get(url)
        if res.ok:
            return res.content

    def get_assignment_name(self, class_id: str, assignment_id: str) -> str:
        """
        Requires you to be a TA of the course.
        """
        r = self.grading_get_rubrics(class_id)
        if r:
            for a in r.get("assignments", []):
                if str(a.get("id")) == assignment_id:
                    return a.get("title")
    
    def get_assignment_id(self, class_id: str, assignment_name: str):
        """
        Requires you to be a TA of the course.
        """
        r = self.grading_get_rubrics(class_id)
        if r:
            for a in r.get("assignments", []):
                if str(a.get("title")) == assignment_name:
                    return a.get("id")

    def student_get_assignment_id(self, class_id: str, assignment_name: str):
        pass
        #TODO IMPL ME

    def submit_via_repo(self, class_id: str, assignment_id: str, method: str, repo_identifier: str, branch: str, leaderboard_name: str="", owner_id: str=None):
        """
        The full branch name MUST be correct
        Also method must be either github or bitbucket
        repo_identifier must be the repo id for github or the project name for bitbucket.
        """
        if not self.logged_in:
            print("You must be logged in!")
            return
        refurl = self.base_url + f"/courses/{class_id}"
        url = refurl + f"/assignments/{assignment_id}/submissions"
        token = self.get_token(refurl, meta="csrf-token")
        payload = {
            "utf8": "✓",
            "authenticity_token": token,
            "submission[method]": method,
            "submission[repository]": repo_identifier,
            "submission[revision]": branch,
            "submission[leaderboard_name]": leaderboard_name
        }
        if owner_id is not None:
            payload["submission[owner_id]"] = owner_id
        self.last_res = res = self.submit_form(url, url, data=payload)
        return res.ok
            

    def get_bitbucket_branches(self, project_name: str):
        """
        E.g. https://www.gradescope.com/bitbucket_projects/ThaumicMekanism/cs61c-lab0_with_git/branches
        """
        if not self.logged_in:
            print("You must be logged in!")
            return
        url = f"https://www.gradescope.com/bitbucket_projects/{project_name}/branches"
        self.last_res = res = self.session.get(url)
        if res.ok:
            return json.loads(res.content)

    def get_bitbucket_projects(self):
        if not self.logged_in:
            print("You must be logged in!")
            return
        url = "https://www.gradescope.com/bitbucket_projects"
        self.last_res = res = self.session.get(url)
        if res.ok:
            return json.loads(res.content)

    def get_github_branches(self, repo_id: str):
        """
        """
        if not self.logged_in:
            print("You must be logged in!")
            return
        url = f"https://www.gradescope.com/github_repositories/{repo_id}/branches"
        self.last_res = res = self.session.get(url)
        if res.ok:
            return json.loads(res.content)

    def get_github_projects(self):
        if not self.logged_in:
            print("You must be logged in!")
            return
        url = "https://www.gradescope.com/github_repositories"
        self.last_res = res = self.session.get(url)
        if res.ok:
            return json.loads(res.content)

    def get_submission_roster(self, class_id: str, assignment_id: str):
        if not self.logged_in:
            print("You must be logged in!")
            return
        url = self.base_url + f"/courses/{class_id}/assignments/{assignment_id}/submissions"
        self.last_res = res = self.session.get(url)
        if not res.ok:
            return
        self.last_soup = soup = BeautifulSoup(res.content, "html.parser")
        cdata = GS_CDATA_decoder(soup=soup)
        return cdata.get_gon().get("roster")