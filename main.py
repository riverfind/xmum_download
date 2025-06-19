from moodel_module import XmumMoodle, get_fzf_selection
import sys

xmum = XmumMoodle()

if len(sys.argv) == 1:
    xmum.print_courses()
else:
    match sys.argv[1]:
        case 'cs':
            xmum.print_courses()

        case 'cc':
            course = xmum.fetch_course(get_fzf_selection([item['name'] for item in xmum.courses_list]))
            course.print_resources()

        case "dld":
            course = xmum.fetch_course(get_fzf_selection([item['name'] for item in xmum.courses_list]))
            course.download(get_fzf_selection(name for name in course.content_list.keys()))
        case _:
            print("Error No such command")
