import requests
from bs4 import BeautifulSoup
import json
from rich.console import Console
from rich.table import Table
from dotenv import load_dotenv, main
import os
import subprocess
from rich.progress import Progress, DownloadColumn, TransferSpeedColumn
from urllib.parse import urlparse, unquote

def get_fzf_selection(options):
    process = subprocess.Popen(
        ['fzf'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        text=True
    )

    stdout, _ = process.communicate('\n'.join(options))
    return stdout.strip()

class Course:
    content_list = []
    def __init__(self, target_resources_list, monitor):
        self.content_list = target_resources_list
        self.__monitor = monitor

    def print_resources(self):
        table = Table(title="FILEs")

        table.add_column("NAME", justify="left", style="cyan", no_wrap=True)
        table.add_column("URL", style="magenta")
        
        for entry_name, entry_url in self.content_list.items():
            table.add_row(entry_name, entry_url)

        self.__monitor.console.print(table)

    def download(self, file_name):
        response_resource = self.__monitor.session.get(self.content_list[file_name], stream=True)
        resource_name = os.path.basename(urlparse(unquote(response_resource.url)).path)
        
        with Progress(
            "[progress.description]{task.description}",
            DownloadColumn(),
            TransferSpeedColumn(),
            "[progress.percentage]{task.percentage:>3.0f}%",
        ) as progress:
            task = progress.add_task(f"{resource_name} Downloading...", total=None)
            with open(resource_name, "wb") as file:
                for chunk in response_resource.iter_content(chunk_size=1024):
                    if chunk:
                        file.write(chunk)
                        progress.update(task, advance = len(chunk))

class XmumMoodle:
    courses_list = []
    console = None
    def __init__(self):
        load_dotenv()
        self.__credential = {}
        self.__credential["username"] = [os.getenv('ac')]
        self.__credential['password'] = [os.getenv('ps')]
        self.console = Console()
        self.__base_url = "https://l.xmu.edu.my"
        self.__login_url = self.__base_url + "/login/index.php"
        
        self.session = requests.Session()
        tmp_response = self.session.get(self.__login_url)
        tmp_soup = BeautifulSoup(tmp_response.content, "lxml")

        self.__credential["logintoken"] = (tmp_soup.find("input", attrs={"name": "logintoken"}))["value"]
        response_login = self.session.post(self.__login_url, data=self.__credential)


        login_sucess_soup = BeautifulSoup(response_login.content, "lxml")
        self.__sesskey = (login_sucess_soup.find("input", attrs={"name": "sesskey"}))["value"]


        user_id = login_sucess_soup.find(
            "div", attrs={"class": "block-recentlyaccessedcourses block-cards"}
        )["data-userid"]


        self.__ajax_service_base_url = "https://l.xmu.edu.my/lib/ajax/service.php?"
        self.__sesskey_prefix = "sesskey="
        self.__sesskey_setting = self.__sesskey_prefix + self.__sesskey
        self.__method_prefix = "info="
        method_setting = (
            self.__method_prefix + "core_course_get_enrolled_courses_by_timeline_classification"
        )
        ajax_courses_list_url = self.__ajax_service_base_url + self.__sesskey_setting + "&" + method_setting


        self.__headers = {"Content-Type": "application/json", "X-Requested-With": "XMLHttpRequest"}

        course_req_payload = [
            {
                "index": 0,
                "methodname": "core_course_get_enrolled_courses_by_timeline_classification",
                "args": {
                    "classification": "all",
                    "customfieldname": "",
                    "customfieldvalue": "",
                    "limit": 0,
                    "offset": 0,
                    "sort": "ul.timeaccess desc",
                },
            }
        ]


        course_list_response = self.session.post(ajax_courses_list_url, json=course_req_payload, headers=self.__headers)



        course_list_data = (json.loads(course_list_response.content))[0]["data"]["courses"]


        self.courses_list = []
        for course in course_list_data:
            self.courses_list.append(
                {"name": course["fullname"], "url": course["viewurl"], "id": course["id"]}
            )

    def print_courses(self):
        table = Table(title="COURSE")

        table.add_column("NAME", justify="left", style="cyan", no_wrap=True)
        table.add_column("URL", style="magenta")
        table.add_column("id", justify="center", style="green")
        
        for entry in self.courses_list:
            table.add_row(entry['name'], entry['url'], str(entry['id']))

        self.console.print(table)

    def fetch_course(self, course_name):

        target_course = None
        for course in self.courses_list:
            if course_name == course["name"]:
                target_course = course

        get_course_data = [
            {
                "index": 0,
                "methodname": "core_courseformat_get_state",
                "args": {"courseid": target_course["id"]},
            }
        ]

        ajax_target_course_content_url = (
            self.__ajax_service_base_url
            + self.__sesskey_setting
            + "&"
            + self.__method_prefix
            + "core_courseformat_get_state"
        )


        target_course_content = self.session.get(
            ajax_target_course_content_url, json=get_course_data, headers=self.__headers
        )


        target_course_data_str = json.loads(target_course_content.content)[0]["data"]
        target_course_data = json.loads(target_course_data_str)


        target_course_resources_list = {}
        for item in target_course_data["cm"]:
            if item["module"] == "resource":
                target_course_resources_list[item["name"]] = item["url"]

        return Course(target_course_resources_list, self)


if __name__ == "__main__":
    xmum = XmumMoodle()
    xmum.print_courses()

    course = xmum.fetch_course(get_fzf_selection([item['name'] for item in xmum.courses_list]))
    course.print_resources()
    
    course.download(get_fzf_selection(name for name in course.content_list.keys()))


