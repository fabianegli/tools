from textwrap import dedent

from textual.app import ComposeResult
from textual.containers import Center
from textual.screen import Screen
from textual.widgets import Button, Footer, Header, Markdown

github_text_markdown = """
# Create a GitHub repo

After creating the pipeline template locally, we can create a GitHub repository and push the code to it.

Do you want to create a GitHub repository?
"""


class GithubRepoQuestion(Screen):
    """Ask if the user wants to create a GitHub repository."""

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        yield Markdown(dedent(github_text_markdown))
        yield Center(
            Button("Create GitHub repo", id="github_repo", variant="success"),
            Button("Finish without creating a repo", id="exit", variant="primary"),
            classes="cta",
        )
