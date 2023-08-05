import click

import grid.globals as env
import grid.commands.checks as checks


def monkey_patch_click(*args, **kwargs):
    pass


def test_check_if_uncommited_files(monkeypatch):
    """
    Grid._check_if_uncommited_files() shows prompts if uncommited
    files are found
    """
    def monkey_pach_git_command(*args, **kwargs):
        return 'test_0.txt: needs update\ntest_1.txt: needs update'

    monkeypatch.setattr(checks, 'execute_git_command', monkey_pach_git_command)
    monkeypatch.setattr(click, 'confirm', monkey_patch_click)

    # Make sure that we are not ignoring warnings.
    env.IGNORE_WARNINGS = False
    result = checks.WorkflowChecksMixin._check_if_uncommited_files()
    assert result == True

    _ignore = env.IGNORE_WARNINGS
    env.IGNORE_WARNINGS = True
    result = checks.WorkflowChecksMixin._check_if_uncommited_files()
    assert result == False

    env.IGNORE_WARNINGS = _ignore


def test_check_if_remote_head_is_different(monkeypatch):
    """
    _check_if_remote_head_is_different() checks if remote SHA is
    different than local
    """
    def monkey_patch_git_command_fatal(*args, **kwargs):
        return 'fatal'

    monkeypatch.setattr(checks, 'execute_git_command',
                        monkey_patch_git_command_fatal)
    assert checks.WorkflowChecksMixin._check_if_remote_head_is_different(
    ) is None

    def monkey_patch_git_command_same(*args, **kwargs):
        return 'foo'

    monkeypatch.setattr(checks, 'execute_git_command',
                        monkey_patch_git_command_same)
    assert checks.WorkflowChecksMixin._check_if_remote_head_is_different(
    ) == False
