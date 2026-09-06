import pytest, re
from universal_remote.lib.display.screen_learning import LearnScreen
from universal_remote.lib.core.types import ProgrammableButtons


def assert_text_called_with_specific_text_once(frame_buffer, text: str):
    text_call_args = [call[0][0] for call in frame_buffer.text.call_args_list]
    arg_matches = re.findall(rf"{re.escape(text)}'", str(text_call_args))
    assert len(arg_matches) == 1


@pytest.fixture
def buttons():
    return [button for button in dir(ProgrammableButtons()) if button[0:2] != "__"]


class TestLearningScreen:
    class TestLearningScreen:
        def test_build_learning_screen_contains_the_button_to_be_learned(self, buttons):
            screen = LearnScreen(remote="Remote 1", buttons=buttons)

            screen.build_learning(selected_button=2, battery_charge=3)

            assert_text_called_with_specific_text_once(screen.frame_buffer, "Remote 1")
            assert_text_called_with_specific_text_once(screen.frame_buffer, buttons[2])

        def test_build_learning_screen_always_contains_a_button_to_be_learned(
            self, buttons
        ):
            screen = LearnScreen(remote="Remote 1", buttons=buttons)

            screen.build_learning(battery_charge=3)

            assert_text_called_with_specific_text_once(screen.frame_buffer, buttons[0])

        def test_build_learning_screen_handles_long_remote_names(self, buttons):
            name = "Remote with an unfortunately long name"
            screen = LearnScreen(remote=name, buttons=buttons)

            screen.build_learning(selected_button=0, battery_charge=3)

            assert_text_called_with_specific_text_once(screen.frame_buffer, name[:20])

    class TestLearnedScreen:
        def test_build_learned_screen_displays_learned_info(self, buttons):
            screen = LearnScreen(remote="Remote 1", buttons=buttons)

            screen.build_learned(
                selected_button=1,
                id=6,
                address=7,
                press_command=8,
                release_command=9,
                battery_charge=4,
            )

            assert_text_called_with_specific_text_once(screen.frame_buffer, buttons[1])
            assert_text_called_with_specific_text_once(screen.frame_buffer, "6")
            assert_text_called_with_specific_text_once(screen.frame_buffer, "7")
            assert_text_called_with_specific_text_once(screen.frame_buffer, "8")
            assert_text_called_with_specific_text_once(screen.frame_buffer, "9")

        def test_build_learned_screen_handles_long_remote_names(self, buttons):
            name = "Remote with an unfortunately long name"
            screen = LearnScreen(remote=name, buttons=buttons)

            screen.build_learned(
                selected_button=1,
                id=6,
                address=7,
                press_command=8,
                release_command=9,
                battery_charge=4,
            )

            assert_text_called_with_specific_text_once(screen.frame_buffer, name[:20])
