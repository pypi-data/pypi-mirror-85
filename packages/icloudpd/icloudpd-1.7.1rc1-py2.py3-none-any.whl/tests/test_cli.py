# coding=utf-8
from unittest import TestCase
import os
import shutil
from vcr import VCR
import pytest
from click.testing import CliRunner
from icloudpd.base import main

vcr = VCR(decode_compressed_response=True)


class CliTestCase(TestCase):
    @pytest.fixture(autouse=True)
    def inject_fixtures(self, caplog):
        self._caplog = caplog

    def test_cli(self):
        runner = CliRunner()
        result = runner.invoke(main, ["--help"])
        assert result.exit_code == 0

    def test_log_levels(self):
        if not os.path.exists("tests/fixtures/Photos"):
            os.makedirs("tests/fixtures/Photos")

        parameters = [
            ("debug", ["DEBUG", "INFO"], []),
            ("info", ["INFO"], ["DEBUG"]),
            ("error", [], ["DEBUG", "INFO"]),
        ]
        for log_level, expected, not_expected in parameters:
            self._caplog.clear()
            with vcr.use_cassette("tests/vcr_cassettes/listing_photos.yml"):
                # Pass fixed client ID via environment variable
                os.environ["CLIENT_ID"] = "DE309E26-942E-11E8-92F5-14109FE0B321"
                runner = CliRunner()
                result = runner.invoke(
                    main,
                    [
                        "--username",
                        "jdoe@gmail.com",
                        "--password",
                        "password1",
                        "--recent",
                        "0",
                        "--log-level",
                        log_level,
                        "-d"
                        "tests/fixtures/Photos",
                    ],
                )
                assert result.exit_code == 0
            for text in expected:
                self.assertIn(text, self._caplog.text)
            for text in not_expected:
                self.assertNotIn(text, self._caplog.text)

    def test_tqdm(self):
        if not os.path.exists("tests/fixtures/Photos"):
            os.makedirs("tests/fixtures/Photos")
        with vcr.use_cassette("tests/vcr_cassettes/listing_photos.yml"):
            # Force tqdm progress bar via ENV var
            os.environ["FORCE_TQDM"] = "yes"
            runner = CliRunner()
            result = runner.invoke(
                main,
                [
                    "--username",
                    "jdoe@gmail.com",
                    "--password",
                    "password1",
                    "--recent",
                    "0",
                    "-d",
                    "tests/fixtures/Photos",
                ],
            )
            del os.environ["FORCE_TQDM"]
            assert result.exit_code == 0

    def test_unicode_directory(self):
        with vcr.use_cassette("tests/vcr_cassettes/listing_photos.yml"):
            # Pass fixed client ID via environment variable
            os.environ["CLIENT_ID"] = "DE309E26-942E-11E8-92F5-14109FE0B321"
            runner = CliRunner()
            result = runner.invoke(
                main,
                [
                    "--username",
                    "jdoe@gmail.com",
                    "--password",
                    "password1",
                    "--recent",
                    "0",
                    "--log-level",
                    "info",
                    "-d",
                    "tests/fixtures/相片",
                ],
            )
            assert result.exit_code == 0

    def test_missing_directory(self):
        base_dir = os.path.normpath("tests/fixtures/Photos")
        if os.path.exists(base_dir):
            shutil.rmtree(base_dir)

        runner = CliRunner()
        result = runner.invoke(
            main,
            [
                "--username",
                "jdoe@gmail.com",
                "--password",
                "password1",
                "--recent",
                "0",
                "--log-level",
                "info",
                "-d",
                base_dir
            ],
        )
        assert result.exit_code == 2

    def test_missing_directory_param(self):
        runner = CliRunner()
        result = runner.invoke(
            main,
            [
                "--username",
                "jdoe@gmail.com",
                "--password",
                "password1",
                "--recent",
                "0",
                "--log-level",
                "info",
            ],
        )
        assert result.exit_code == 2
