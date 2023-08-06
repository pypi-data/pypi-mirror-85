import time
from io import BytesIO
import zipfile
import yaml

class GS_autograder:
    def __init__(self, client: "GradescopeClient", class_id: str, assignment_id: str):
        self.client = client
        self.class_id = class_id
        self.assignment_id = assignment_id
        self.docker_id = None
        self.last_data = {}
        self.last_json_data = {}
    
    def recheck(self, recheck):
        if recheck or not self.last_data:
            self.last_data = self.client.ag_building_data(self.class_id, self.assignment_id)
            self.docker_id = self.get_id(recheck=False)
        
    def recheck_json(self, recheck):
        if self.docker_id is None:
            self.recheck(True)
        if recheck or not self.last_json_data:
            self.last_json_data = self.client.get_docker_image(self.class_id, self.assignment_id, self.docker_id)
    
    def is_building_from_configure_ag(self, recheck=True) -> bool:
        self.recheck(recheck)
        AG_BUILDING = "autograder_building"
        return AG_BUILDING in self.last_data and self.last_data[AG_BUILDING]

    def is_configured(self, recheck=True) -> bool:
        self.recheck(recheck)
        AG_CONFIGURED = "autograder_configured"
        return AG_CONFIGURED in self.last_data and self.last_data[AG_CONFIGURED]

    def get_status(self, recheck=True):
        self.recheck_json(recheck)
        AG_STATUS = "status"
        if AG_STATUS in self.last_json_data:
            return self.last_json_data[AG_STATUS]
        
    def is_building(self, recheck=True):
        return self.get_status(recheck=recheck) == "building"

    def is_built(self, recheck=True):
        return self.get_status(recheck=recheck) == "built"
    
    def build_failed(self, recheck=True):
        return self.get_status(recheck=recheck) == "failed"

    def get_image(self, recheck=True) -> dict:
        self.recheck(recheck)
        AG_IMAGE = "image"
        if AG_IMAGE not in self.last_data:
            return {}
        return self.last_data[AG_IMAGE]
    
    def get_id(self, recheck=True) -> str:
        self.recheck(recheck)
        AG_ID = "id"
        img = self.get_image(recheck=False)
        if img is None or AG_ID not in img:
            return None
        return img[AG_ID]

    def get_stdout(self, recheck=True) -> str:
        self.recheck_json(recheck)
        AG_STDOUT = "stdout"
        if AG_STDOUT in self.last_json_data:
            return self.last_json_data[AG_STDOUT]

    def get_stderr(self, recheck=True) -> str:
        self.recheck_json(recheck)
        AG_STDERR = "stderr"
        if AG_STDERR in self.last_json_data:
            return self.last_json_data[AG_STDERR]
    
    def rebuild_and_print_output(self, file_name: str, print_fn=print, check_interval: int=1, timeout: int=600, force_rebuilt: bool=False) -> bool:
        did_rebuild = True
        if force_rebuilt or not self.is_building():
            did_rebuild = self.client.rebuild_autograder(self.class_id, self.assignment_id, file_name)
        if not did_rebuild:
            print("[ERROR]: Failed to start the autograder rebuild!")
        start = time.time()
        dont_continue = self.is_building()
        stdout_so_far = ""
        def update_stdout(recheck=True):
            nonlocal stdout_so_far
            stdout = self.get_stdout(recheck=recheck)
            if isinstance(stdout, str):
                new_stdout = stdout[len(stdout_so_far):]
                if len(new_stdout) > 0:
                    print_fn(new_stdout, end="")
                    stdout_so_far = stdout
        update_stdout(recheck=False)
        while dont_continue:
            time.sleep(check_interval)
            time_since_start = time.time() - start
            update_stdout()
            dont_continue = self.is_building(recheck=False) and (timeout is not None and time_since_start < timeout)
        update_stdout()
        stderr = self.get_stderr(recheck=False)
        if stderr:
            print_fn(stderr)
        return self.is_built(recheck=False)

    def set_manual_configuration(self, image: str) -> bool:
        return self.client.set_manual_ag_config(self.class_id, self.assignment_id, image)

    def regrade_all(self) -> bool:
        return self.client.regrade_all(self.class_id, self.assignment_id)

    def regrade_submission(self, submission_id: str) -> bool:
        return self.client.regrade_submission(self.class_id, self.assignment_id, submission_id)

    def export_submissions(self, force_export: bool=False) -> bytes:
        file_id = None
        if not force_export:
            print("Checking if an export has already been created...")
            gon_report = self.client.check_gon_export_submissions_progress(self.class_id, self.assignment_id)
            if gon_report:
                file_id = gon_report.get("id")
        if file_id is None:
            print("Starting a new export...")
            file_id = self.client.start_export_submissions(self.class_id, self.assignment_id)
            print(f"Export started for file id {file_id}!")
            if not file_id:
                print("Failed to start the submission export!")
                return
            completed = False
            while not completed:
                res = self.client.check_export_submissions_progress(self.class_id, file_id)
                if not res:
                    print("Got bad response when checking progress!")
                    return
                percentage = "{:.0%}".format(res.get("progress"))
                print(f"Export Progress: {percentage}", end="\r")
                completed = res.get("status") == "completed"
                if not completed:
                    # Gradescope default rechecks every 5 seconds.
                    time.sleep(1)
            print("\nExport Finished!")
        else:
            print(f"Export already available ({file_id})!")

        return self.client.download_export_submissions(self.class_id, file_id)

    def export_autograder_metadata(self):
        data = self.export_submissions()
        if not data:
            print("Failed to export submission data!")
            return
        zipdata = BytesIO(data)
        zf = zipfile.ZipFile(zipdata)
        meta = zf.open(f"assignment_{self.assignment_id}_export/submission_metadata.yml")
        sub_meta = yaml.load(meta, Loader=yaml.FullLoader)
        return sub_meta

    def download_scores(self):
        return self.client.download_scores(self.class_id, self.assignment_id)
