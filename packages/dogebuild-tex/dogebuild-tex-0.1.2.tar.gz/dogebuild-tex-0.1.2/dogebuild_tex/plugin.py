import os
import platform
from pathlib import Path, PosixPath, WindowsPath
from shutil import rmtree
from subprocess import run
from typing import List

from dogebuild.plugins import DogePlugin


class TexBinary:
    def get_pdf_command(self, build_dir: Path, out_file_name: str, main_file: Path) -> List[str]:
        raise NotImplementedError()


class SystemTexBinary(TexBinary):
    def __init__(self, pdf_binary: str = "pdflatex"):
        self.pdf_binary = pdf_binary

    def get_pdf_command(self, build_dir: Path, out_file_name: str, main_file: Path) -> List[str]:
        return [
            self.pdf_binary,
            f"-output-directory={build_dir}",
            f"-jobname={out_file_name}",
            main_file,
        ]


class DockerTexBinary(TexBinary):
    def __init__(self, image: str, version: str = "latest", pdf_binary: str = "pdflatex"):
        self.image = image
        self.version = version
        self.pdf_binary = pdf_binary

    def get_pdf_command(self, build_dir: Path, out_file_name: str, main_file: Path) -> List[str]:
        command = ["docker", "run", "--rm"]

        system = platform.system()
        if system != "Windows":
            uid = os.getuid()
            gid = os.getgid()
            command.extend(["--user", f"{uid}:{gid}"])

        command.extend(["-v", f"{self.to_docker_path_str(build_dir)}:{self.to_docker_path_str(build_dir)}"])

        cwd = self.to_docker_path_str(Path(os.getcwd()))
        command.extend(["-v", f"{cwd}:{cwd}"])
        command.extend(["-w", cwd])

        command.append(f"{self.image}:{self.version}")
        command.append(self.pdf_binary)

        command.append(f"-output-directory={self.to_docker_path_str(build_dir)}")
        command.append(f"-jobname={out_file_name}")
        command.append(self.to_docker_path_str(main_file))

        return command

    @staticmethod
    def to_docker_path_str(path: Path):
        if isinstance(path, WindowsPath):
            drive = path.parts[0]
            rest = path.parts[1:]
            drive_letters = drive[: -len(":\\")].lower()
            return f"/{drive_letters}/" + "/".join(rest)
        elif isinstance(path, PosixPath):
            return str(path)
        else:
            raise NotImplementedError(f"Not implemented for {path.__class__.__name__}")


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

        command = self.tex_binary.get_pdf_command(self.build_dir, self.out_file_name, self.main_file)
        result = run(command)

        return result.returncode, {"pdf": [out_file]}

    def clean(self):
        rmtree(self.build_dir)
