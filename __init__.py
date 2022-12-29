# -*- coding: utf-8 -*-

# Copyright (c) 2016 Kura
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from __future__ import unicode_literals
from uuid import uuid4

from docutils import nodes
from docutils.parsers.rst import directives, Directive


def align(argument):
    """Conversion function for the "align" option."""
    return directives.choice(argument, ("left", "center", "right"))


class Lightbox(Directive):
    """
    Create a pure CSS lightbox for images.

    Usage:

        .. lightbox::
            :thumb: /images/test-thumb.png
            :large: /images/test.png
            :alt: This is a test image
            :caption: A test caption
            :align: center
    """

    required_arguments = 0
    optional_arguments = 3
    option_spec = {
        "thumb": str,
        "large": str,
        "alt": str,
        "caption": str,
        "align": align,
        "div_class": str,
        "image_class": str,
        "a_class": str,
        "caption_class": str,
    }

    final_argument_whitespace = False
    has_content = False

    def run(self):
        """Run the directive."""
        if "thumb" not in self.options:
            raise self.error("Thumb argument is required.")
        thumb = self.options["thumb"]
        if "large" not in self.options:
            raise self.error("Large argument is required.")
        large = self.options["large"]

        uuid = str(uuid4())

        align = self.options.get("align", "left")

        div_class = self.options.get("div_class", None)
        if div_class is None:
            div_class = ""
        if div_class and align:
            div_class = f'{div_class} align-{align}'
        elif align:
            div_class = f'align-{align}'

        image_class = self.options.get("image_class", None)
        if image_class is None:
            image_class = ""

        a_class = self.options.get("a_class", None)
        if a_class is None:
            a_class = ""

        caption_class = self.options.get("caption_class", None)
        if caption_class is None:
            caption_class = ""

        alt_text = self.options.get("alt", None)
        if alt_text is None:
            alt_text = "Click to view large image"

        caption = self.options.get("caption", None)
        if caption is None:
            caption = 'Click to view large image'

        block = (
            f'<div class="lightbox-block {div_class}">'
            f'  <a href="#{uuid}" title="{alt_text}">'
            f'    <img src="{thumb}" alt="{alt_text}" class="{image_class}"/>'
            f'  </a>'
            f'  <a href="#_" class="lightbox" id="{uuid}" '
            f'     title="Click to close">'
            f'    <img alt="Click to close" src="{large}"/>'
            f'  </a>'
            f'  <p class="lightbox-caption {caption_class}">{caption}</p>'
            f'  <div class="lightbox-divider"></div>'
            f'</div>'
        )
        return [nodes.raw("", block, format="html")]


def register():
    """Register the directive."""
    directives.register_directive("lightbox", Lightbox)
