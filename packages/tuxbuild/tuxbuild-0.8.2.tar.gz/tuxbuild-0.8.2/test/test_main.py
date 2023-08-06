# -*- coding: utf-8 -*-

import tuxbuild.__main__


def test_run(monkeypatch, mocker):
    run = tuxbuild.__main__.run
    main = mocker.patch("tuxbuild.__main__.main")
    monkeypatch.setattr(tuxbuild.__main__, "__name__", "__main__")
    run()
    main.assert_called()
