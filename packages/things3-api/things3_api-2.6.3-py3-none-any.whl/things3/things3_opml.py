#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""OPML Plugin for the Thing 3 CLI."""

from __future__ import print_function

__author__ = "Alexander Willner"
__copyright__ = "2020 Alexander Willner"
__credits__ = ["Alexander Willner"]
__license__ = "Apache License 2.0"
__version__ = "2.6.3"
__maintainer__ = "Alexander Willner"
__email__ = "alex@willner.ws"
__status__ = "Development"

import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element, SubElement
from xml.dom import minidom


class Things3OPML():
    """OPML Plugin for Thing 3 CLI."""

    @staticmethod
    def get_top():
        """Get first element."""
        top = Element('opml')
        head = SubElement(top, 'head')
        title = SubElement(head, 'title')
        title.text = 'Things 3 Database'
        return top

    @staticmethod
    def print(top):
        """Print pretty XML."""
        xmlstr = minidom.parseString(
            ET.tostring(top)).toprettyxml(indent="   ")
        print(xmlstr)

    def print_tasks(self, tasks):
        """Print pretty XML of selected tasks."""
        top = self.get_top()
        body = SubElement(top, 'body')
        for task in tasks:
            SubElement(body, 'outline').set('text', task['title'])
        self.print(top)

    def print_all(self, things3):
        """Print."""
        top = self.get_top()
        body = SubElement(top, 'body')

        for area in things3.get_areas():
            area_element = SubElement(body, 'outline')
            area_element.set('text', area['title'])
            for task in things3.get_task(area['uuid']):
                SubElement(area_element, 'outline').set('text', task['title'])
            for project in things3.get_projects(area['uuid']):
                project_element = SubElement(area_element, 'outline')
                project_element.set('text', project['title'])
                for task in things3.get_task(None, project['uuid']):
                    SubElement(project_element, 'outline').set(
                        'text', task['title'])
        self.print(top)
