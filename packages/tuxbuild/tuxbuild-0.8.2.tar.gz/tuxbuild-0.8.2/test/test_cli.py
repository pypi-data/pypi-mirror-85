# -*- coding: utf-8 -*-

from click.testing import CliRunner
import pytest
import tuxbuild.cli
import tuxbuild.build

sample_token = "Q9qMlmkjkIuIGmEAw-Mf53i_qoJ8Z2eGYCmrNx16ZLLQGrXAHRiN2ce5DGlAebOmnJFp9Ggcq9l6quZdDTtrkw"
sample_url = "https://foo.bar.tuxbuild.com/v1"


def test_usage():
    """ Test running cli() with no arguments """
    runner = CliRunner()
    result = runner.invoke(tuxbuild.cli.cli, [])
    assert result.exit_code == 0
    assert "Usage" in result.output
    assert "Commands" in result.output


def test_build_no_args():
    """ Test calling build() with no options """
    runner = CliRunner()
    result = runner.invoke(tuxbuild.cli.build, [])
    assert result.exit_code == 2
    assert "Usage" in result.output
    assert "help" in result.output


def test_build_usage():
    """ Test calling build() with --help """
    runner = CliRunner()
    result = runner.invoke(tuxbuild.cli.build, ["--help"])
    assert result.exit_code == 0
    assert "Usage" in result.output
    assert "--toolchain" in result.output
    assert "--git-repo TEXT" in result.output


@pytest.fixture
def tuxbuild_config(tmp_path, monkeypatch):
    c = tmp_path / "config.ini"
    with c.open("w") as f:
        f.write("[default]\n")
        f.write(f"token={sample_token}\n")
        f.write(f"api_url={sample_url}\n")
    monkeypatch.setenv("TUXBUILD_CONFIG", str(c))
    return c


def test_build(mocker, tuxbuild_config):
    build = mocker.patch("tuxbuild.Build.build")
    wait_for_object = mocker.patch("tuxbuild.cli.wait_for_object")
    runner = CliRunner()
    result = runner.invoke(
        tuxbuild.cli.build,
        [
            "--git-repo=https://git.example.com/linux.git",
            "--git-ref=master",
            "--target-arch=arm64",
            "--kconfig=defconfig",
            "--toolchain=gcc-9",
        ],
    )
    assert result.exit_code == 0
    assert build.call_count == 1
    assert wait_for_object.call_count == 1


def test_build_quiet(mocker, tuxbuild_config):
    Build = mocker.patch("tuxbuild.Build")
    Build.return_value.build_data = "https://tuxbuild.example.com/abcdef0123456789/"
    mocker.patch("tuxbuild.cli.wait_for_object")
    runner = CliRunner()
    result = runner.invoke(
        tuxbuild.cli.build,
        [
            "--git-repo=https://git.example.com/linux.git",
            "--git-ref=master",
            "--target-arch=arm64",
            "--kconfig=defconfig",
            "--toolchain=gcc-9",
            "--quiet",
        ],
    )
    assert result.exit_code == 0
    assert "Building Linux Kernel" not in result.output
    assert result.output == "https://tuxbuild.example.com/abcdef0123456789/\n"


def test_build_git_sha(mocker, tuxbuild_config):
    build = mocker.patch("tuxbuild.Build.build")
    wait_for_object = mocker.patch("tuxbuild.cli.wait_for_object")
    runner = CliRunner()
    result = runner.invoke(
        tuxbuild.cli.build,
        [
            "--git-repo=https://git.example.com/linux.git",
            "--git-sha=beefbee",
            "--target-arch=arm64",
            "--kconfig=defconfig",
            "--toolchain=gcc-9",
        ],
    )
    assert result.exit_code == 0
    assert build.call_count == 1
    assert wait_for_object.call_count == 1


def test_build_git_head(mocker, tuxbuild_config):
    get_git_head = mocker.patch("tuxbuild.gitutils.get_git_head")
    get_git_head.return_value = ("https://example.com/linux.git", "deadbeef")
    Build = mocker.patch("tuxbuild.Build")
    Build.return_value.build_data = "https://tuxbuild.example.com/abcdef0123456789/"
    wait_for_object = mocker.patch("tuxbuild.cli.wait_for_object")

    runner = CliRunner()
    result = runner.invoke(
        tuxbuild.cli.build,
        [
            "--git-head",
            "--target-arch=arm64",
            "--kconfig=defconfig",
            "--toolchain=gcc-9",
        ],
    )
    Build.assert_called_with(
        git_repo="https://example.com/linux.git",
        git_sha="deadbeef",
        git_ref=None,
        target_arch="arm64",
        kconfig=("defconfig",),
        kconfig_allconfig=None,
        toolchain="gcc-9",
    )
    wait_for_object.assert_called()
    assert result.exit_code == 0


def test_build_download(mocker, tuxbuild_config):
    build = mocker.patch("tuxbuild.Build.build")
    wait_for_object = mocker.patch("tuxbuild.cli.wait_for_object")
    download = mocker.patch("tuxbuild.download.download")
    runner = CliRunner()
    result = runner.invoke(
        tuxbuild.cli.build,
        [
            "--git-repo=https://git.example.com/linux.git",
            "--git-ref=master",
            "--target-arch=arm64",
            "--kconfig=defconfig",
            "--toolchain=gcc-9",
            "--download",
        ],
    )
    assert result.exit_code == 0
    assert build.call_count == 1
    assert wait_for_object.call_count == 1
    download.assert_called_with(mocker.ANY, ".")


def test_build_download_output_dir(mocker, tuxbuild_config, tmp_path):
    mocker.patch("tuxbuild.Build.build")
    mocker.patch("tuxbuild.cli.wait_for_object")
    download = mocker.patch("tuxbuild.download.download")
    runner = CliRunner()
    result = runner.invoke(
        tuxbuild.cli.build,
        [
            "--git-repo=https://git.example.com/linux.git",
            "--git-ref=master",
            "--target-arch=arm64",
            "--kconfig=defconfig",
            "--toolchain=gcc-9",
            "--download",
            f"--output-dir={tmp_path}",
        ],
    )
    assert result.exit_code == 0
    download.assert_called_with(mocker.ANY, str(tmp_path))


def test_build_show_logs(mocker, tuxbuild_config):
    Build = mocker.patch("tuxbuild.Build")
    build = Build.return_value
    build.build_data = "https://builds.com/21321312312/"
    wait_for_object = mocker.patch("tuxbuild.cli.wait_for_object")
    download_file = mocker.patch("tuxbuild.download.download_file")
    runner = CliRunner()
    result = runner.invoke(
        tuxbuild.cli.build,
        [
            "--git-repo=https://git.example.com/linux.git",
            "--git-ref=master",
            "--target-arch=arm64",
            "--kconfig=defconfig",
            "--toolchain=gcc-9",
            "--show-logs",
        ],
    )
    assert result.exit_code == 0
    assert build.build.call_count == 1
    assert wait_for_object.call_count == 1
    download_file.assert_called_with(
        "https://builds.com/21321312312/build.log", mocker.ANY
    )


def test_build_download_show_logs(mocker, tuxbuild_config, tmp_path):
    Build = mocker.patch("tuxbuild.Build")
    build = Build.return_value
    build.build_key = "21321312312"
    build.build_data = "https://builds.com/21321312312/"
    wait_for_object = mocker.patch("tuxbuild.cli.wait_for_object")
    runner = CliRunner()
    (tmp_path / "21321312312").mkdir()
    (tmp_path / "21321312312" / "build.log").write_text(
        "log line 1\nlog line 2\nerror: something\n"
    )
    result = runner.invoke(
        tuxbuild.cli.build,
        [
            "--git-repo=https://git.example.com/linux.git",
            "--git-ref=master",
            "--target-arch=arm64",
            "--kconfig=defconfig",
            "--toolchain=gcc-9",
            "--download",
            f"--output-dir={tmp_path}",
            "--show-logs",
        ],
    )
    assert result.exit_code == 0
    assert build.build.call_count == 1
    assert wait_for_object.call_count == 1
    assert "log line 1\nlog line 2\n" in result.output
    assert "error: something" in result.output


sample_build_set = """
sets:
  - name: test
    builds:
      - {target_arch: arm64, toolchain: gcc-9, kconfig: defconfig}
      - {target_arch: arm64, toolchain: gcc-9, kconfig: allmodconfig}
      - {target_arch: arm64, toolchain: gcc-9, kconfig: allyesconfig}
      - {target_arch: arm, toolchain: gcc-9, kconfig: allmodconfig}
      - {target_arch: x86_64, toolchain: gcc-9, kconfig: allmodconfig}
      - {target_arch: x86_64, toolchain: clang-9, kconfig: allmodconfig}
      - {target_arch: x86_64, toolchain: gcc-9, kconfig: allyesconfig}
      - {target_arch: i386, toolchain: gcc-9, kconfig: allmodconfig}
      - {target_arch: riscv, toolchain: gcc-9, kconfig: allyesconfig}
  - name: arch-matrix
    builds:
      - {target_arch: arm64,  toolchain: gcc-9}
      - {target_arch: arm,    toolchain: gcc-9}
      - {target_arch: i386,   toolchain: gcc-9}
      - {target_arch: riscv,  toolchain: gcc-9}
      - {target_arch: x86_64,    toolchain: gcc-9}
"""


@pytest.fixture
def tux_config(tmp_path):
    config = tmp_path / "buildset.yaml"
    with config.open("w") as f:
        f.write(sample_build_set)
    return config


def test_build_set(mocker, tuxbuild_config, tux_config):
    build = mocker.patch("tuxbuild.BuildSet.build")
    wait_for_object = mocker.patch("tuxbuild.cli.wait_for_object")
    runner = CliRunner()
    result = runner.invoke(
        tuxbuild.cli.build_set,
        [
            "--git-repo=https://git.example.com/linux.git",
            "--git-ref=master",
            f"--tux-config={tux_config}",
            "--set-name=test",
        ],
    )
    assert result.exit_code == 0
    assert build.call_count == 1
    assert wait_for_object.call_count == 1


def test_build_set_no_kconfig(mocker, tuxbuild_config, tux_config):
    build = mocker.patch("tuxbuild.BuildSet.build")
    wait_for_object = mocker.patch("tuxbuild.cli.wait_for_object")
    runner = CliRunner()
    result = runner.invoke(
        tuxbuild.cli.build_set,
        [
            "--git-repo=https://git.example.com/linux.git",
            "--git-ref=master",
            f"--tux-config={tux_config}",
            "--set-name=arch-matrix",
            "--quiet",
        ],
    )
    build.assert_not_called()
    wait_for_object.assert_not_called()
    assert result.exit_code == 1
    assert "kconfig is mandatory" in result.output


def test_build_set_quiet(mocker, tuxbuild_config, tux_config):
    BuildSet = mocker.patch("tuxbuild.BuildSet")
    builds = []
    for i in range(1, 10):
        build = mocker.MagicMock()
        build.build_data = f"https://tuxbuild.example.com/{i}/"
        builds.append(build)
    BuildSet.return_value.builds = builds
    mocker.patch("tuxbuild.cli.wait_for_object")
    runner = CliRunner()
    result = runner.invoke(
        tuxbuild.cli.build_set,
        [
            "--git-repo=https://git.example.com/linux.git",
            "--git-ref=master",
            f"--tux-config={tux_config}",
            "--set-name=test",
            "--quiet",
        ],
    )
    assert result.exit_code == 0
    output = "".join([f"https://tuxbuild.example.com/{i}/\n" for i in range(1, 10)])
    assert result.output == output


def test_build_set_git_sha(mocker, tuxbuild_config, tux_config):
    build = mocker.patch("tuxbuild.BuildSet.build")
    wait_for_object = mocker.patch("tuxbuild.cli.wait_for_object")
    runner = CliRunner()
    result = runner.invoke(
        tuxbuild.cli.build_set,
        [
            "--git-repo=https://git.example.com/linux.git",
            "--git-sha=beefbee",
            f"--tux-config={tux_config}",
            "--set-name=test",
            "--quiet",
        ],
    )
    assert result.exit_code == 0
    assert build.call_count == 1
    assert wait_for_object.call_count == 1


def test_build_set_download(mocker, tuxbuild_config, tux_config):
    build = mocker.patch("tuxbuild.BuildSet.build")
    wait_for_object = mocker.patch("tuxbuild.cli.wait_for_object")
    download = mocker.patch("tuxbuild.download.download")
    runner = CliRunner()
    result = runner.invoke(
        tuxbuild.cli.build_set,
        [
            "--git-repo=https://git.example.com/linux.git",
            "--git-ref=master",
            f"--tux-config={tux_config}",
            "--set-name=test",
            "--download",
        ],
    )
    assert result.exit_code == 0
    assert build.call_count == 1
    assert wait_for_object.call_count == 1
    assert download.call_count == 9


def test_build_set_show_logs(mocker, tuxbuild_config, tux_config):
    build = mocker.patch("tuxbuild.BuildSet.build")
    wait_for_object = mocker.patch("tuxbuild.cli.wait_for_object")
    show_log = mocker.patch("tuxbuild.cli.show_log")
    runner = CliRunner()
    result = runner.invoke(
        tuxbuild.cli.build_set,
        [
            "--git-repo=https://git.example.com/linux.git",
            "--git-ref=master",
            f"--tux-config={tux_config}",
            "--set-name=test",
            "--show-logs",
        ],
    )
    assert result.exit_code == 0
    assert build.call_count == 1
    assert wait_for_object.call_count == 1
    assert show_log.call_count == 9


def state(mocker, **kwargs):
    s = mocker.MagicMock()

    # defaults
    s.state = "completed"
    s.status = "pass"
    s.icon = "✓"
    s.cli_color = "white"
    s.errors = 0
    s.warnings = 0
    s.final = True

    for k, v in kwargs.items():
        setattr(s, k, v)

    return s


@pytest.fixture
def build_state(mocker):
    return state(mocker)


def test_wait_for_object_pass(mocker, build_state):
    build = mocker.MagicMock()
    build.watch.return_value = [build_state]
    assert tuxbuild.cli.wait_for_object(build)


def test_wait_for_object_pass_with_warnings(mocker, build_state):
    build = mocker.MagicMock()
    build_state.warnings = 1
    build.watch.return_value = [build_state]
    assert tuxbuild.cli.wait_for_object(build)


def test_wait_for_object_fail(mocker, build_state):
    build = mocker.MagicMock()
    build_state.status = "fail"
    build_state.errors = 1
    build.watch.return_value = [build_state]
    assert not tuxbuild.cli.wait_for_object(build)


def test_wait_for_object_infra_failure(mocker, build_state):
    build = mocker.MagicMock()
    build_state.state = "error"
    build.final = True
    build.watch.return_value = [build_state]
    assert not tuxbuild.cli.wait_for_object(build)


def test_wait_for_object_infra_failure_retried(mocker):
    error = state(mocker, state="error", final=False)
    retry_pass = state(mocker)
    build = mocker.MagicMock()
    build.watch.return_value = [error, retry_pass]
    assert tuxbuild.cli.wait_for_object(build)
