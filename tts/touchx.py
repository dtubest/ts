import argparse
import os
import sys


def find_template(name):
    file = name + ".ts"
    ts = os.path.join(user_template_path, file)
    if os.path.isfile(ts):
        return ts

    sys_ts = os.path.join(sys_template_path, name)
    if os.path.isfile(sys_ts):
        return sys_ts

    return False


class TemplateAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        ts = find_template(values)

        if ts:
            setattr(namespace, "ts", ts)
            setattr(namespace, self.dest, values)

        else:
            self.report_missing(values)
            sys.exit()

    @staticmethod
    def report_missing(name):
        print("template %s not found" % name)


user_template_path = os.path.expanduser("~/.ts")
sys_template_path = "/etc/ts"


def main():
    parser = argparse.ArgumentParser(description="touches executable scripts")
    parser.add_argument("-t", "--template", action=TemplateAction, help="template used to create files");
    parser.add_argument("files", nargs="+", help="scripts to be created")

    options = parser.parse_args()

    for file in options.files:
        if os.path.isfile(file):
            print("%s already exists, ignore" % file)
            continue

        if hasattr(options, 'ts'):
            os.system("cat %s > %s" % (options.ts, file))
        else:
            os.system("touch " + file)

        os.chmod(file, 0o751)
