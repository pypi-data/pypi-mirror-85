# Copyright 2020 The SQLNet Company GmbH

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to
# deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
# sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

"""
Collection of functions for visualizing the data model
that are not intended to be used by
the end-user.
"""

from getml import constants

from .relationship import many_to_many

TABLE_WIDTH = 150
TABLE_HEIGHT = 90

LABEL_WIDTH = 150
LABEL_HEIGHT = 70

LINE_COLOR = "#808080;"


def _make_horizontal_icon_line(origin, length):
    line = """<div """
    line += """style="height:3px;"""
    line += """px;"""
    line += """width:"""
    line += str(length)
    line += """px;background-color:#ffffff;"""
    line += """position:absolute;top:"""
    line += str(origin[0])
    line += """px;left:"""
    line += str(origin[1])
    line += """px;"""
    line += """"></div>"""
    return line


def _make_vertical_icon_line(origin, length):
    line = """<div """
    line += """style="height:"""
    line += str(length)
    line += """px;"""
    line += """width:3px;"""
    line += """background-color:#ffffff;"""
    line += """position:absolute;top:"""
    line += str(origin[0])
    line += """px;left:"""
    line += str(origin[1])
    line += """px;""
    line += """"></div>"""
    return line


def _make_icon(origin, size=48):
    icon = """<div """
    icon += """style="height:"""
    icon += str(size)
    icon += """px;"""
    icon += """width:"""
    icon += str(size)
    icon += """px;"""
    icon += """border-style: solid;"""
    icon += """border-radius:10%;"""
    icon += """border-width:3px;"""
    icon += """border-color:#ffffff;"""
    icon += """position:absolute;top:"""
    icon += str(origin[0])
    icon += """px;left:"""
    icon += str(origin[1])
    icon += """px;"""
    icon += """"></div>"""

    icon += _make_vertical_icon_line(
        (origin[0], origin[1] + size/3 - 1), size)

    icon += _make_vertical_icon_line(
        (origin[0],
         origin[1] + 2*size/3 - 2), size)

    icon += _make_horizontal_icon_line(
        (origin[0] + size/3 - 1, origin[1]), size)

    icon += _make_horizontal_icon_line(
        (origin[0] + 2*size/3 - 2, origin[1]), size)

    return icon


def _make_table(name, origin):
    table = """<div """
    table += """style="height:"""
    table += str(TABLE_HEIGHT)
    table += """px;"""
    table += """width:"""
    table += str(TABLE_WIDTH)
    table += """px;"""
    table += """background-color:#6829c2;"""
    table += """color:#ffffff;"""
    table += """text-align:center;position:absolute;top:"""
    table += str(origin[0])
    table += """px;left:"""
    table += str(origin[1])
    table += """px;border-radius:5%;"><div style="margin-top:65px;">"""
    table += name
    table += """</div></div>"""

    table += _make_icon((origin[0] + 10, origin[1] + 51))

    return table


def _make_horizontal_line(origin, length):
    line = """<div """
    line += """style="height:4px;"""
    line += """width:"""
    line += str(length)
    line += """px;background-color:"""
    line += LINE_COLOR + ";"
    line += """color:#ffffff;"""
    line += """text-align:center;"""
    line += """position:absolute;top:"""
    line += str(origin[0])
    line += """px;left:"""
    line += str(origin[1])
    line += """px;border-radius:5%;">"""
    line += """</div>"""
    return line


def _make_vertical_line(origin, length):
    line = """<div """
    line += """style="height:"""
    line += str(length)
    line += """px;width:4px;"""
    line += """background-color:"""
    line += LINE_COLOR + ";"
    line += """;color:#ffffff;"""
    line += """text-align:center;"""
    line += """position:absolute;top:"""
    line += str(origin[0])
    line += """px;left:"""
    line += str(origin[1])
    line += """px;border-radius:5%;">"""
    line += """</div>"""
    return line


def _make_triangle_down(origin):
    triangle = """<div style=" """
    triangle += """width: 0;"""
    triangle += """height: 0;"""
    triangle += """border-left: 7px solid transparent;"""
    triangle += """border-right: 7px solid transparent;"""
    triangle += """border-top: 14px solid """
    triangle += LINE_COLOR + "; "
    triangle += """position:absolute;top:"""
    triangle += str(origin[0])
    triangle += """px;left:"""
    triangle += str(origin[1] - 5)
    triangle += """px;">"""
    triangle += "</div>"
    return triangle


def _make_triangle_right(origin):
    triangle = """<div style=" """
    triangle += """width: 0;"""
    triangle += """height: 0;"""
    triangle += """border-top: 7px solid transparent;"""
    triangle += """border-left: 15px solid """
    triangle += LINE_COLOR + ";"
    triangle += """border-bottom: 7px solid transparent;"""
    triangle += """position:absolute;top:"""
    triangle += str(origin[0])
    triangle += """px;left:"""
    triangle += str(origin[1] - 5)
    triangle += """px;">"""
    triangle += "</div>"
    return triangle


def _make_label(content, origin):
    table = """<div """
    table += """style="height:"""
    table += str(LABEL_HEIGHT)
    table += """px;"""
    table += """width:"""
    table += str(LABEL_WIDTH)
    table += """px;"""
    table += """background-color:#6829c2;"""
    table += """color:#ffffff;"""
    table += """text-align:center;"""
    table += """line-height: 1.0;"""
    table += """display:table;"""
    table += """position:absolute;top:"""
    table += str(origin[0])
    table += """px;left:"""
    table += str(origin[1])
    table += """px;border-radius:5%;">"""
    table += """<div style="display:table-cell;vertical-align:middle;font-size:10px;">"""
    table += content
    table += """</div></div>"""
    return table


def _make_arrow(label, origin, target):

    adj_origin = (origin[0] + TABLE_HEIGHT / 2 - 2, origin[1] + TABLE_WIDTH)
    adj_target = (target[0], target[1] + TABLE_WIDTH / 2 - 2)
    if origin[0] == target[0]:
        adj_target = (target[0] + TABLE_HEIGHT / 2, target[1] - 2)

    label_pos0 = adj_origin[0] - LABEL_HEIGHT / 2 + 2

    if origin[0] == target[0]:
        label_pos1 = adj_origin[1] + \
            (adj_target[1] - adj_origin[1] - LABEL_WIDTH) / 2
    else:
        label_pos1 = adj_origin[1] + (adj_target[1] -
                                      adj_origin[1] - LABEL_WIDTH) / 2 - TABLE_WIDTH / 4

    arrow = _make_horizontal_line(adj_origin, adj_target[1] - adj_origin[1])
    arrow += _make_vertical_line((adj_origin[0], adj_target[1]),
                                 adj_target[0] - adj_origin[0] - 3)

    if origin[0] == target[0]:
        arrow += _make_triangle_right((adj_target[0] - 7, adj_target[1] - 5))
    else:
        arrow += _make_triangle_down((adj_target[0] - 12, adj_target[1]))

    arrow += _make_label(label, (label_pos0, label_pos1))

    return arrow


def _split_multiple_join_keys(multiple):
    multiple = multiple.replace(constants.MULTIPLE_JOIN_KEYS_BEGIN, "")
    multiple = multiple.replace(constants.MULTIPLE_JOIN_KEYS_END, "")
    return multiple.split(constants.JOIN_KEY_SEP)


def _make_join_keys(placeholder, i):

    if constants.JOIN_KEY_SEP in placeholder.join_keys_used[i]:
        join_keys = _split_multiple_join_keys(placeholder.join_keys_used[i])
        other_join_keys = _split_multiple_join_keys(
            placeholder.other_join_keys_used[i])

        if len(join_keys) != len(other_join_keys):
            raise ValueError("Number of join keys does not match!")

        return [other + " = " + jk for other, jk in zip(other_join_keys, join_keys)]

    return [placeholder.other_join_keys_used[i] + " = " + placeholder.join_keys_used[i]]


def _make_time_stamps(placeholder, i):
    lines = []

    lines += [
        placeholder.other_time_stamps_used[i] +
        " <= " + placeholder.time_stamps_used[i]
    ]

    if placeholder.upper_time_stamps_used[i] != "":
        lines += [
            placeholder.upper_time_stamps_used[i] +
            " > " + placeholder.time_stamps_used[i]
        ]

    return lines


def _make_window(diff):
    seconds_per_day = 24.0 * 60.0 * 60.0
    seconds_per_hour = 60.0 * 60.0
    seconds_per_minute = 60.0

    window_formatted = str(diff) + " seconds"

    if diff >= seconds_per_day:
        window_formatted = str(diff / seconds_per_day) + " days"

    elif diff >= seconds_per_hour:
        window_formatted = str(diff / seconds_per_hour) + " hours"

    elif diff >= seconds_per_minute:
        window_formatted = str(diff / seconds_per_minute) + " minutes"

    return window_formatted


def _make_label_content(placeholder, i):
    lines = []

    if placeholder.join_keys_used[i] != "$GETML_NO_JOIN_KEY":
        lines += _make_join_keys(placeholder, i)

    if placeholder.time_stamps_used[i] != "":
        lines += _make_time_stamps(placeholder, i)

    if placeholder.memory[i] > 0.0:
        lines += ["Memory: " + _make_window(placeholder.memory[i])]

    if placeholder.horizon[i] != 0.0:
        lines += ["Horizon: " + _make_window(placeholder.horizon[i])]

    if placeholder.allow_lagged_targets[i]:
        lines += ["Lagged targets allowed"]

    if placeholder.relationship[i] != many_to_many:
        lines += ["Relationship: " + placeholder.relationship[i]]

    if not lines:
        return "1 = 1"

    return "<br>".join(lines)


class _DataModel:

    def __init__(self, placeholder):
        self.rectangles = []
        self.links = []

        self.height = 0
        self.width = 0

        self._make_structure(0, placeholder)
        self._calc_positions()
        self._calc_size()

    def _add_children(self, depth, placeholder):
        child_ids = []

        for joined_table in placeholder.joined_tables:
            if len(joined_table.joined_tables) > 0:
                self._make_structure(depth + 1, joined_table)
            else:
                self._add_placeholder(depth + 1, joined_table)

            child_ids += [len(self.rectangles) - 1]

        return child_ids

    def _add_links(self, placeholder, child_ids, parent_id):
        for i, child_id in enumerate(child_ids):
            label = _make_label_content(placeholder, i)
            link = dict()
            link["source_id"] = child_id
            link["target_id"] = parent_id
            link["label"] = label
            self.links += [link]

    def _add_placeholder(self, depth, placeholder):
        rectangle = dict()
        rectangle["depth"] = depth
        rectangle["id"] = len(self.rectangles)
        rectangle["name"] = placeholder.name
        self.rectangles += [rectangle]
        return rectangle["id"]

    def _calc_positions(self):
        max_depth = self._find_max_depth()

        pos0 = 0

        for i, rectangle in enumerate(self.rectangles):

            if i > 0 and rectangle["depth"] >= self.rectangles[i-1]["depth"]:
                pos0 += 110

            pos1 = 500 * (max_depth - rectangle["depth"])

            self.rectangles[i]["pos"] = (pos0, pos1)

    def _calc_size(self):
        last = len(self.rectangles) - 1
        self.height = self.rectangles[last]["pos"][0] + TABLE_HEIGHT
        self.width = self.rectangles[last]["pos"][0] + TABLE_WIDTH

    def _find_max_depth(self):
        max_depth = 0

        for rectangle in self.rectangles:
            if rectangle["depth"] > max_depth:
                max_depth = rectangle["depth"]

        return max_depth

    def _make_structure(self, depth, placeholder):
        child_ids = self._add_children(depth, placeholder)
        parent_id = self._add_placeholder(depth, placeholder)
        self._add_links(placeholder, child_ids, parent_id)

    def to_html(self):
        """
        Expresses the data model in pure HTML code.
        """
        html = """<div style="height:""" + str(self.height) + "px;"
        html += "width:" + str(self.width) + "px;"
        html += """position:relative;">"""

        for rectangle in self.rectangles:
            html += _make_table(rectangle["name"], rectangle["pos"])

        for link in self.links:
            origin = self.rectangles[link["source_id"]]["pos"]
            target = self.rectangles[link["target_id"]]["pos"]
            html += _make_arrow(link["label"], origin, target)

        html += "</div>"

        return html
