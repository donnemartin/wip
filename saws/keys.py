# -*- coding: utf-8 -*-

# Copyright 2015 Donne Martin. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"). You
# may not use this file except in compliance with the License. A copy of
# the License is located at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# or in the "license" file accompanying this file. This file is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
# ANY KIND, either express or implied. See the License for the specific
# language governing permissions and limitations under the License.

from __future__ import unicode_literals
from __future__ import print_function
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.application import run_in_terminal


class KeyManager(object):
    """Creates a Key Manager.

    Attributes:
        * manager: An instance of a prompt_toolkit's KeyBindingManager.
    """

    def __init__(self, set_color, get_color,
                 set_fuzzy_match, get_fuzzy_match,
                 set_shortcut_match, get_shortcut_match,
                 refresh_resources_and_options, handle_docs):
        """Initializes KeyManager.

        Args:
            * set_color: A function setting the color output config.
            * get_color: A function getting the color output config.
            * set_fuzzy_match: A function setting the fuzzy match config.
            * get_fuzzy_match: A function getting the fuzzy match config.
            * set_shortcut_match: A function setting the shortcut match config.
            * get_shortcut_match: A function getting the shortcut match config.

        Returns:
            None.
        """
        self.manager = None
        self.key_bindings = self._create_key_bindings(
            set_color, get_color, set_fuzzy_match, get_fuzzy_match,
            set_shortcut_match, get_shortcut_match,
            refresh_resources_and_options, handle_docs)

    def _create_key_bindings(self, set_color, get_color,
                             set_fuzzy_match, get_fuzzy_match,
                             set_shortcut_match, get_shortcut_match,
                             refresh_resources_and_options, handle_docs):
        """Creates and initializes the keybinding manager.

        Args:
            * set_color: A function setting the color output config.
            * get_color: A function getting the color output config.
            * set_fuzzy_match: A function setting the fuzzy match config.
            * get_fuzzy_match: A function getting the fuzzy match config.
            * set_shortcut_match: A function setting the shortcut match config.
            * get_shortcut_match: A function getting the shortcut match config.

        Returns:
            A KeyBindingManager.
        """
        assert callable(set_color)
        assert callable(get_color)
        assert callable(set_fuzzy_match)
        assert callable(get_fuzzy_match)
        assert callable(set_shortcut_match)
        assert callable(get_shortcut_match)
        assert callable(refresh_resources_and_options)
        assert callable(handle_docs)

        kb = KeyBindings()

        @kb.add('f2')
        def handle_f2(_):
            """Enables/Disables color output.

            Args:
                * _: An instance of prompt_toolkit's Event (not used).

            Returns:
                None.
            """
            set_color(not get_color())

        @kb.add('f3')
        def handle_f3(_):
            """Enables/Disables fuzzy matching.

            Args:
                * _: An instance of prompt_toolkit's Event (not used).

            Returns:
                None.
            """
            set_fuzzy_match(not get_fuzzy_match())

        @kb.add('f4')
        def handle_f4(_):
            """Enables/Disables shortcut matching.

            Args:
                * _: An instance of prompt_toolkit's Event (not used).

            Returns:
                None.
            """
            set_shortcut_match(not get_shortcut_match())

        @kb.add('f5')
        def handle_f5(event):
            """Refreshes AWS resources.

            Args:
                * event: An instance of prompt_toolkit's Event.

            Returns:
                None.
            """
            run_in_terminal(refresh_resources_and_options)

        @kb.add('f9')
        def handle_f9(_):
            """Inputs the "docs" command when the `F9` key is pressed.

            Args:
                * _: An instance of prompt_toolkit's Event (not used).

            Returns:
                None.
            """
            handle_docs(from_fkey=True)

        @kb.add('f10')
        def handle_f10(event):
            """Quits when the `F10` key is pressed.

            Args:
                * _: An instance of prompt_toolkit's Event (not used).

            Returns:
                None.
            """
            event.app.exit()

        @kb.add('c-space')
        def handle_ctrl_space(event):
            """Initializes autocompletion at the cursor.

            If the autocompletion menu is not showing, display it with the
            appropriate completions for the context.

            If the menu is showing, select the next completion.

            Args:
                * event: An instance of prompt_toolkit's Event.

            Returns:
                None.
            """
            b = event.cli.current_buffer
            if b.complete_state:
                b.complete_next()
            else:
                event.cli.start_completion(select_first=False)

        return kb
