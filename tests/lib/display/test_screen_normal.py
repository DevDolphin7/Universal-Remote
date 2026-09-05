import pytest, re
from universal_remote.lib.display.screen_normal import NormalScreen

"""
test_build_learning_screen_contains_the_button_to_be_learned
test_build_learning_screen_contains_screen_dimensions
test_build_learning_screen_always_contains_a_button_to_be_learned
"""


def assert_text_called_with_specific_text_once(frame_buffer, text: str):
    text_call_args = [call[0][0] for call in frame_buffer.text.call_args_list]
    arg_matches = re.findall(rf"{re.escape(text)}'", str(text_call_args))
    assert len(arg_matches) == 1


@pytest.fixture()
def some_remotes():
    return ["Remote 1", "Remote 2", "Remote 3"]


@pytest.fixture()
def many_remotes():
    return [f"Remote {i}" for i in range(16)]


class TestNormalScreen:
    def test_build_normal_screen_contains_learned_remotes(self, some_remotes):
        screen = NormalScreen(menu_items=some_remotes, protocol_name="Protocol 1")
        screen.build(selected_remote=0, battery_charge=3)

        assert screen.protocol_name == "Protocol 1"

        assert len(some_remotes) > 0
        for item in some_remotes:
            assert screen.menu_items.count(item) == 1
            assert_text_called_with_specific_text_once(screen.frame_buffer, item)

    def test_build_normal_screen_contains_screen_dimensions(self, some_remotes):
        screen = NormalScreen(menu_items=some_remotes, protocol_name="Protocol 1")

        assert screen._screen_width == 200
        assert screen._screen_height == 200

    def test_build_normal_screen_handles_empty_remote_list(self):
        screen = NormalScreen(menu_items=[], protocol_name="Protocol 1")
        screen.build(selected_remote=0, battery_charge=3)

        assert screen.menu_items == ["Add New"]
        assert screen.protocol_name == "Protocol 1"

        assert_text_called_with_specific_text_once(screen.frame_buffer, "Add New")
        with pytest.raises(AssertionError):
            assert_text_called_with_specific_text_once(screen.frame_buffer, "Remote ")

    def test_build_normal_screen_handles_long_remote_list(self, many_remotes):
        screen = NormalScreen(menu_items=many_remotes, protocol_name="Protocol 1")
        screen.build(selected_remote=9, battery_charge=3)

        assert len(screen.menu_items) == len(many_remotes) + 1

        assert_text_called_with_specific_text_once(screen.frame_buffer, "Remote 9")
        with pytest.raises(AssertionError):
            assert_text_called_with_specific_text_once(screen.frame_buffer, "Remote 0")

    def test_build_normal_screen_handles_long_remote_names(self):
        long_remote_name = "Remote with a very long name that exceeds the screen width"

        screen = NormalScreen(menu_items=[long_remote_name], protocol_name="Protocol 1")
        screen.build(selected_remote=0, battery_charge=3)

        assert_text_called_with_specific_text_once(
            screen.frame_buffer, long_remote_name[:20]
        )
