from os import getuid, getgid, getcwd
from pathlib import Path
from shutil import rmtree
from subprocess import run
from typing import List

from dogebuild.plugins import DogePlugin


class TexBinary:
    def get_pdf_command(self, *touched_directories: Path) -> List[str]:
        raise NotImplementedError()


class SystemTexBinary(TexBinary):
    def __init__(self, pdf_binary: str = "pdflatex"):
        self.pdf_binary = pdf_binary

    def get_pdf_command(self, *touched_directories: Path) -> List[str]:
        return [self.pdf_binary]


class DockerTexBinary(TexBinary):
    def __init__(self, image: str, version: str = "latest", pdf_binary: str = "pdflatex"):
        self.image = image
        self.version = version
        self.pdf_binary = pdf_binary

    def get_pdf_command(self, *touched_directories: Path) -> List[str]:
        command = ["docker", "run", "--rm", "--user", f"{getuid()}:{getgid()}"]
        for d in touched_directories:
            command.append("-v")
            command.append(f"{d}:{d}")
        command.append("-v")
        command.append(f"{getcwd()}:{getcwd()}")
        command.append("-w")
        command.append(getcwd())
        command.append(f"{self.image}:{self.version}")
        command.append(self.pdf_binary)

        return command


class Tex(DogePlugin):
    NAME = "tex-plugin"

    def __init__(
        self,
        tex_binary: TexBinary = SystemTexBinary(),
        main_file: Path = Path("main.tex").expanduser().resolve(),
        build_dir: Path = Path("build").expanduser().resolve(),
        out_file_name: str = "main",
    ):
        super().__init__()
        self.tex_binary = tex_binary
        self.main_file = main_file
        self.build_dir = build_dir
        self.out_file_name = out_file_name

        self.add_task(self.build_pdf, aliases=["pdf"], phase="build")
        self.add_task(self.clean, phase="clean")

    def build_pdf(self):
        self.build_dir.mkdir(exist_ok=True, parents=True)
        out_file = (self.build_dir / self.out_file_name).with_suffix(".pdf")

        result = run(
            [
                *self.tex_binary.get_pdf_command(self.build_dir),
                f"-output-directory={self.build_dir}",
                f"-jobname={self.out_file_name}",
                self.main_file,
            ]
        )

        return result.returncode, {"pdf": [out_file]}

    def clean(self):
        rmtree(self.build_dir)
