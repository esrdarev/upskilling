#!/usr/bin/env python3
"""
Generator script for the Project Snowden Directed Upskilling Platform static site.
"""

__author__ = "Ashley Phillips/Deakin University"
__version__ = "0.1.0"
__license__ = "None"

import argparse
from fpdf import FPDF
from logzero import logger
from markdown import markdown
from math import floor
import yaml


class PDF(FPDF):
    def lines(self):
        self.set_line_width(0.0)
        self.line(5.0,5.0,205.0,5.0)
        self.line(5.0,292.0,205.0,292.0)
        self.line(5.0,5.0,5.0,292.0)
        self.line(205.0,5.0,205.0,292.0)
    
    def heading(self):
        self.set_font('Arial', 'B', 16)
        self.cell(20, 5, 'Project Snowden', 0, 1, 'L')
        self.set_font('Arial', '', 12)
        self.cell(35, 5, 'Squad Progress Report', 0, 1, 'L')
        self.ln()
        self.ln()

    def details(self, syllabus, squad):
        self.set_font('Arial', 'B', 10)
        
        for module_key in syllabus['modules']:
            module = syllabus['modules'][module_key]
            if 'tasks' not in module.keys():
                continue

            self.add_page()
            self.lines()
            self.heading()

            self.cell(15, 10, module['name'], 0, 0, 'L')
            self.ln()
            self.cell(15, 10, 'Member', 0, 0, 'L')
            for task_key in module['tasks']:
                task = module['tasks'][task_key]
                self.cell(15, 10, task_key, 0, 0, 'C')
            self.ln()
            
            for member_key in squad['members']:
                member = squad['members'][member_key]
                self.cell(15, 10, member_key.upper(), 0, 0, 'L')
                for task_key in module['tasks']:
                    task = module['tasks'][task_key]
                    self.cell(15, 10, 'C', 0, 0, 'C')
                self.ln()


def main(args):
    """ Main entry point of the app """
    logger.info("Starting site generation...")
    logger.info(args)
    logger.info("Opening syllabus.yml...")
    with open("data/syllabus.yml", "r") as syllabus_file:
        syllabus = yaml.safe_load(syllabus_file)

    logger.info("Found the following modules:")
    for module in syllabus['modules']:
        logger.info(f"...{syllabus['modules'][module]['name']}")

    logger.info("Opening squad.yml...")
    with open("data/squad.yml", "r") as squad_file:
        squad = yaml.safe_load(squad_file)

    for member in squad['members']:
        logger.info(f"Found member {member.upper()}")
        logger.info(f"...{squad['members'][member]}")

    logger.info("Processing index.html template...")
    with open("templates/index.html") as index_template_file:
        index_template = index_template_file.read()

    index_template = module_list(index_template, syllabus, squad)
    index_template = task_list(index_template, syllabus, squad)
    index_template = member_progress_list(index_template, syllabus, squad)

    logger.info("Writing completed template out...")
    with open("docs/index.html", "w") as index_output_file:
        index_output_file.write(index_template)

    logger.info("Generating member pages...")
    with open("templates/member-page.html", "r") as member_template_file:
        member_page_template = member_template_file.read()
    generate_member_pages(member_page_template, syllabus, squad)

    logger.info("Generating task detail pages...")
    with open("templates/task-details.html", "r") as task_details_file:
        task_details_template = task_details_file.read()
    generate_task_details_pages(task_details_template, syllabus, squad)

    logger.info("Generating downloads...")
    generate_downloads(syllabus, squad)


def generate_downloads(syllabus, squad):
    # Squad progress download
    squad_pdf = PDF(format='A4', unit='mm')
    squad_pdf.details(syllabus, squad)
    squad_pdf.output('docs/squad_progress.pdf', 'F')


def generate_task_details_pages(task_details_template, syllabus, squad):
    for module_key in syllabus['modules']:
        module = syllabus['modules'][module_key]

        if 'tasks' not in module.keys():
            continue

        for task_key in module['tasks']:
            output = task_details_template
            html = ""
            task = module['tasks'][task_key]
            if 'task_details' in task.keys():
                print(task)
                with open('data/' + task['task_details'], "r") as task_details_markdown:
                    md = task_details_markdown.read()
                    html = markdown(md)
            else:
                html = "Task details not available!"
                
            output = output.replace("{task-details}", html)
            file_name = f"docs/{task_key}-details.html"
            with open(file_name, "w") as task_details_output_file:
                task_details_output_file.write(output)
                    


def generate_member_pages(member_page_template, syllabus, squad):
    for member_key in squad['members']:
        logger.info(f"...page for {member_key}")
        member = squad['members'][member_key]
        generate_member_progress(member_key, member, member_page_template, syllabus, squad)


def generate_member_progress(member_key, member, member_page_template, syllabus, squad):
    file_name = f"docs/{member_key}-progress.html"
    output = member_page_template
    member_progress = ""

    for module_key in syllabus['modules']:
        module = syllabus['modules'][module_key]
        module_rank = get_module_rank(module, member, module_key)
        member_progress +=  "<div class=\"ps_module\">"
        member_progress +=  "    <div class=\"inner\">"
        member_progress +=  "        <div class=\"text\">"
        member_progress += f"            <i class=\"{module['font-awesome-icon']} id-color\"></i>"
        member_progress += f"            <h3>{module['name']}</h3> {module['description']}"
        member_progress +=  "            <div class=\"ps_module_rank\">"
        member_progress += f"                <div class=\"ps_module_rank_icon {module_rank}\"></div>"
        member_progress +=  "            </div>"

        member_progress += get_member_module_progress(module, member, module_key)

        member_progress +=  "        </div>"
        member_progress +=  "    </div>"
        member_progress +=  "</div>"

    output = output.replace("{member_progress}", member_progress)
    with open(file_name, "w") as progress_page:
        progress_page.write(output)


def get_member_task_status(module, task, task_key, member):
    # print(task)
    # print(task_key)
    # print(member)

    # No member tasks at all - cannot have started
    if 'tasks' not in member.keys():
        return "incomplete"

    if task_key in member['tasks']:
        if 'date-complete' in member['tasks'][task_key].keys():
            return ""
    
    return "incomplete"


def get_member_module_progress(module, member, module_key):
    output = ""
    if 'tasks' not in module.keys():
        return "";

    for task_key in module['tasks']:
        task = module['tasks'][task_key]
        task_status = get_member_task_status(module, task, task_key, member)
        output +=  "<div class=\"ps_task\">"
        output += f"    <div class=\"ps_task_icon\">"
        output += f"        <div class=\"ps_task_icon_img {task_status}\"></div>"
        output += f"        <span>{task_key}</span>"
        output +=  "        <br />"
        output += f"        <span>{task['name']}</span>"
        output +=  "    </div>"
        output +=  "</div>"
    
    return output


def get_module_rank(module, member, module_key):
    # not-started
    # started
    # halfway
    # complete

    # If there are no module tasks yet, cannot have started!
    if "tasks" not in module.keys():
        return "not-started"

    # If the squad member has no tasks, cannot have started!
    if member['tasks'] == "None":
        return "not-started"

    # Get all tasks in the module we are looking at into a list
    module_tasks = []
    for task in module['tasks']:
        module_tasks.append(task)

    # Get all the tasks COMPLETED by this member
    member_tasks = []
    for task_key in member['tasks']:
        task = member['tasks'][task_key]
        if 'date-complete' in task.keys():
            member_tasks.append(task_key)

    # Get all tasks NOT completed by this member
    member_tasks_to_go = []
    for task in module_tasks:
        if task not in member_tasks:
            member_tasks_to_go.append(task)

    if len(member_tasks) == 0:
        return "not-started"

    if len(member_tasks_to_go) == 0:
        return "complete"

    if len(member_tasks_to_go) <= len(member_tasks):
        return "halfway"

    if len(member_tasks) > 0:
        return "started"
    

def get_task_from_code(code, syllabus):
    for module_key in syllabus['modules']:
        module = syllabus['modules'][module_key]
        for task_key in module['tasks']:
            if task_key == code:
                return module['tasks'][task_key]
    return None


def member_progress_list(index_template, syllabus, squad):
    logger.info("...generating member progress")
    member_progress = ""

    for member_key in squad['members']:
        latest_task = None
        latest_task_code = None
        member = squad['members'][member_key]
        if member['tasks'] == "None":
            latest_task = "None"
            latest_task_long = "Not started yet"
        else:
            latest_task_code = list(member['tasks'])[-1]
            latest_task = get_task_from_code(latest_task_code, syllabus)
            latest_task_long = f"Latest Task: {latest_task['long_designation']}"
            # print(latest_task_long)

        member_progress +=  "<div class=\"bloglist s1 item\">"
        member_progress +=  "    <div class=\"post-content\">"
        member_progress +=  "        <div class=\"date-box\">"
        member_progress += f"            <div class=\"d\">{member_key.upper()}</div>"
        member_progress += f"            <div class=\"m\">{latest_task_code}</div>"
        member_progress +=  "        </div>"
        member_progress +=  "        <div class=\"post-text\">"
        member_progress += f"            <h3><a href=\"{member_key}-progress.html\">{latest_task_long}</a></h3>"
        member_progress += f"            <p>Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt.</p>"
        member_progress +=  "        </div>"
        member_progress +=  "    </div>"
        member_progress +=  "</div>"

    index_template = index_template.replace("{member_progress_list}", member_progress)
    return index_template


def task_list(index_template, syllabus, squad):
    logger.info("...generating task list")
    task_module_list = ""
    task_list = ""

    for module_key in syllabus['modules']:
        module = syllabus['modules'][module_key]
        task_module_list += f"<li><span>{module['name']}</span></li>"
        task_list += "<div class=\"tab_single_content\">"
        if 'tasks' in module.keys():
            for task_key in module['tasks']:
                task = module['tasks'][task_key]
                task_list +=  "    <div class=\"exp-box\">"
                task_list += f"        <h5><a href=\"{task_key}-details.html\">{task['long_designation']}</a></h5>"
                task_list += f"        <h4>{task['name']}</h4>"
                task_list += f"        <p>{task['short_description']}</p>"
                task_list +=  "    </div>"
        else:
            task_list += f"<h3>The {module['name']} syllabus is currently being finalised. Please check back soon!"
        task_list += "</div>"
            
    index_template = index_template.replace("{task_module_list}", task_module_list)
    index_template = index_template.replace("{task_list}", task_list)
    return index_template


def module_list(index_template, syllabus, squad):
    logger.info("...generating modules list")
    module_list = ""

    for module_key in syllabus['modules']:
        module = syllabus['modules'][module_key]
        module_list += f"<!-- service box begin -->"
        module_list += f"<div class=\"feature-box mb30\">"
        module_list += f"    <div class=\"inner\">"
        module_list += f"        <div class=\"text\">"
        module_list += f"            <i class=\"{module['font-awesome-icon']} id-color\"></i>"
        module_list += f"            <h3>{module['name']}</h3> {module['description']}"
        module_list += f"        </div>"
        module_list += f"        <i class=\"big fab {module['font-awesome-icon']} id-color\"></i>"
        module_list += f"    </div>"
        module_list += f"</div>"
        module_list += f"<!-- service box close -->"

    index_template = index_template.replace("{MODULES_LIST}", module_list)
    return index_template


if __name__ == "__main__":
    """ This is executed when run from the command line """
    parser = argparse.ArgumentParser()

    # Optional argument flags which defaults to False
    # - Run in test mode - no updates to "/docs" folder.
    parser.add_argument("-t", "--test", action="store_true", default=False)
    args = parser.parse_args()
    main(args)