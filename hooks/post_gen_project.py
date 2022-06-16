# -*- coding: UTF-8 -*-

"""
1. Renames webpage stylesheet to style.css according to themes selection and deletes unused theme style
"""

import os
import shutil
import traceback

# Get the root project directory
PROJECT_DIRECTORY = os.path.realpath(os.path.curdir)


def rename_selected_theme_file():
    """
    Renames the selected theme css file to style css (from style_white.css or style_blue.css)
    """
    try:
        if "{{ cookiecutter.theme }}" == "white":
            # white header theme
            os.rename(os.path.join(PROJECT_DIRECTORY, 'webpage', 'static', 'webpage', 'css', 'style_white.css'),
                      os.path.join(PROJECT_DIRECTORY, 'webpage', 'static', 'webpage', 'css', 'style.css'))
        else:
            # default blue header theme
            os.rename(os.path.join(PROJECT_DIRECTORY, 'webpage', 'static', 'webpage', 'css', 'style_blue.css'),
                      os.path.join(PROJECT_DIRECTORY, 'webpage', 'static', 'webpage', 'css', 'style.css'))
    except Exception as error:
        traceback.print_exc(f"Error: {error}, {traceback.format_exc()}")


def delete_unused_theme_files():
    """
        Deletes unused theme files
    """
    theme_dir = os.path.join(PROJECT_DIRECTORY, 'webpage', 'static', 'webpage', 'css')
    try:
        for unused_theme in os.listdir(theme_dir):
            if unused_theme.startswith("style_"):
                os.remove(os.path.join(theme_dir, unused_theme))
    except Exception as error:
        traceback.print_exc(f"Error: {error}, {traceback.format_exc()}")


rename_selected_theme_file()
delete_unused_theme_files()
