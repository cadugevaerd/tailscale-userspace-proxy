from __future__ import annotations

import argparse
import sys
import unittest
from pathlib import Path
from types import SimpleNamespace
from typing import Any
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from tailscale_proxy import cli  # noqa: E402


def args(**overrides: object) -> argparse.Namespace:
    values: dict[str, Any] = {
        "yes": False,
        "non_interactive": False,
        "install_claude_code_docker_mcp": False,
        "copy_claude_code_docker_mcp_command": False,
        "copy_claude_code_docker_mcp_wsl_command": False,
        "skip_claude_code_docker_mcp": False,
    }
    values.update(overrides)
    return argparse.Namespace(**values)


class PrerequisitePromptTests(unittest.TestCase):
    def test_negative_answer_cancels_installation(self) -> None:
        with patch("builtins.input", return_value="n"):
            with self.assertRaises(cli.CliError) as caught:
                cli.confirm_or_cancel(args(), "Install uv now?", "uv installation cancelled.")
        self.assertEqual(str(caught.exception), "uv installation cancelled.")

    def test_yes_flag_skips_prompt(self) -> None:
        with patch("builtins.input") as input_mock:
            cli.confirm_or_cancel(args(yes=True), "Install uv now?", "uv installation cancelled.")
        input_mock.assert_not_called()

    def test_non_interactive_without_yes_fails_closed(self) -> None:
        with self.assertRaises(cli.CliError) as caught:
            cli.confirm_or_cancel(args(non_interactive=True), "Install Docker now?", "Docker installation cancelled.")
        self.assertIn("Rerun with --yes", str(caught.exception))

    def test_missing_uv_prompts_then_installs_when_user_accepts(self) -> None:
        state = {"uv_installed": False}

        def command_exists(name: str) -> bool:
            return state["uv_installed"] if name == "uv" else True

        def install_uv(_args: argparse.Namespace) -> None:
            state["uv_installed"] = True

        with patch("builtins.input", return_value="y") as input_mock:
            with patch.object(cli, "command_exists", side_effect=command_exists):
                with patch.object(cli, "install_uv", side_effect=install_uv) as install_mock:
                    with patch.object(cli, "run", return_value=SimpleNamespace(stdout="uv 0.test\n")):
                        cli.ensure_uv_ready(args())

        input_mock.assert_called_once()
        install_mock.assert_called_once()
        self.assertTrue(state["uv_installed"])

    def test_missing_docker_prompts_and_cancels_before_installing(self) -> None:
        with patch.object(cli, "command_exists", return_value=False):
            with patch("builtins.input", return_value="no") as input_mock:
                with patch.object(cli, "install_docker_engine") as install_mock:
                    with self.assertRaises(cli.CliError) as caught:
                        cli.ensure_docker_ready(args())
        self.assertEqual(str(caught.exception), "Docker installation cancelled.")
        input_mock.assert_called_once()
        install_mock.assert_not_called()

    def test_missing_compose_prompts_and_cancels_before_installing(self) -> None:
        with patch.object(cli, "docker_compose_cmd", return_value=None):
            with patch("builtins.input", return_value="n") as input_mock:
                with patch.object(cli, "install_docker_compose") as install_mock:
                    with self.assertRaises(cli.CliError) as caught:
                        cli.ensure_docker_compose_ready(args())
        self.assertEqual(str(caught.exception), "Docker Compose installation cancelled.")
        input_mock.assert_called_once()
        install_mock.assert_not_called()

    def test_claude_code_docker_mcp_negative_answer_skips_without_cancel(self) -> None:
        with patch("builtins.input", return_value="n") as input_mock:
            with patch.object(cli, "install_claude_code_docker_mcp") as install_mock:
                cli.maybe_install_claude_code_docker_mcp(args())
        input_mock.assert_called_once()
        install_mock.assert_not_called()

    def test_claude_code_docker_mcp_positive_answer_installs(self) -> None:
        with patch("builtins.input", return_value="s") as input_mock:
            with patch.object(cli, "install_claude_code_docker_mcp") as install_mock:
                cli.maybe_install_claude_code_docker_mcp(args())
        input_mock.assert_called_once()
        install_mock.assert_called_once()

    def test_claude_code_docker_mcp_non_interactive_skips_by_default(self) -> None:
        with patch("builtins.input") as input_mock:
            with patch.object(cli, "install_claude_code_docker_mcp") as install_mock:
                cli.maybe_install_claude_code_docker_mcp(args(non_interactive=True))
        input_mock.assert_not_called()
        install_mock.assert_not_called()

    def test_claude_code_docker_mcp_copy_answer_prints_local_command(self) -> None:
        with patch("builtins.input", return_value="c") as input_mock:
            with patch.object(cli, "copy_to_clipboard", return_value=True) as copy_mock:
                with patch.object(cli, "install_claude_code_docker_mcp") as install_mock:
                    cli.maybe_install_claude_code_docker_mcp(args())
        input_mock.assert_called_once()
        install_mock.assert_not_called()
        copy_mock.assert_called_once_with("claude mcp add docker-mcp -s user -- uvx docker-mcp")

    def test_claude_code_docker_mcp_wsl_answer_prints_wsl_command(self) -> None:
        with patch("builtins.input", return_value="w") as input_mock:
            with patch.object(cli, "copy_to_clipboard", return_value=False) as copy_mock:
                with patch.object(cli, "install_claude_code_docker_mcp") as install_mock:
                    cli.maybe_install_claude_code_docker_mcp(args())
        input_mock.assert_called_once()
        install_mock.assert_not_called()
        copy_mock.assert_called_once_with("claude mcp add docker-mcp -s user -- wsl.exe -- uvx docker-mcp")

    def test_claude_code_docker_mcp_copy_flag_skips_prompt(self) -> None:
        with patch("builtins.input") as input_mock:
            with patch.object(cli, "copy_to_clipboard", return_value=True) as copy_mock:
                cli.maybe_install_claude_code_docker_mcp(args(copy_claude_code_docker_mcp_command=True))
        input_mock.assert_not_called()
        copy_mock.assert_called_once_with("claude mcp add docker-mcp -s user -- uvx docker-mcp")

    def test_claude_code_docker_mcp_explicit_flag_runs_claude_command(self) -> None:
        def command_exists(name: str) -> bool:
            return name in {"claude", "uvx"}

        with patch.object(cli, "command_exists", side_effect=command_exists):
            with patch.object(cli, "stream", return_value=0) as stream_mock:
                cli.install_claude_code_docker_mcp(args(install_claude_code_docker_mcp=True))
        stream_mock.assert_called_once_with(
            ["claude", "mcp", "add", "docker-mcp", "-s", "user", "--", "uvx", "docker-mcp"],
            check=False,
        )

    def test_claude_code_docker_mcp_requires_claude_cli(self) -> None:
        with patch.object(cli, "command_exists", return_value=False):
            with self.assertRaises(cli.CliError) as caught:
                cli.install_claude_code_docker_mcp(args(install_claude_code_docker_mcp=True))
        self.assertIn("Claude Code CLI", str(caught.exception))


if __name__ == "__main__":
    unittest.main()
