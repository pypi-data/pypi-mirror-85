#! /usr/bin/python3

import argparse, sys, os

from ..core import Project
from cliprint import *


class GitPMDetails:

    """
    'gitpm details' is a tool display project details.
    """

    @staticmethod
    def error(e):
        GitPMDetails.parser.error(e)

    @staticmethod
    def generateParser():

        """
        Generate the ArgumentParser for 'gitpm details'.
        """

        GitPMDetails.parser = argparse.ArgumentParser(
            prog="gitpm [project] details",
            description="Display details of a project.",
            epilog="More details at https://github.com/finnmglas/gitPM.",
        )

        return GitPMDetails.parser

    @staticmethod
    def main(args=None, path=os.getcwd()):

        """
        The main program of 'gitpm details'.
        """

        if args == None:  # parse args using own parser
            GitPMDetails.generateParser()
            args = GitPMDetails.parser.parse_args(sys.argv[1:])

        project = Project(args.project)

        branch = project.getCurrentBranch()
        print(
            color.foreground.BOLD
            + "Project\t"
            + color.foreground.WHITE
            + project.getName()
            + color.END
            + color.foreground.BOLD
            + " pid-"
            + project.getId()
            + " "
            + Project.status_colors[project.getStatus()]
            + project.getStatus()
            + color.END
            + "\n"
        )
        print("About:\t" + project.getDescription() + "")
        print("Tags:\t" + project.getTags() + "\n")
        print("Branch:\t" + branch)
        print("Commit:\t" + project.getLastCommit(branch))


if __name__ == "__main__":
    GitPMDetails.main()
