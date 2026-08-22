"""Hermetic tests for cdb_session's TTD-capable cdb.exe discovery."""

from __future__ import annotations

from mcp_windbg import debug_session
from mcp_windbg.cdb_session import DEFAULT_CDB_PATHS, DEFAULT_CDB_TTD_PATHS, find_ttd_cdb


def test_find_ttd_cdb_returns_none_when_no_windows_apps_build_exists(monkeypatch):
    monkeypatch.setattr(debug_session.os.path, "isfile", lambda p: False)
    assert find_ttd_cdb() is None


def test_find_ttd_cdb_prefers_cdbx64_over_the_other_architectures(monkeypatch):
    x64, x86, arm64 = DEFAULT_CDB_TTD_PATHS
    monkeypatch.setattr(debug_session.os.path, "isfile", lambda p: p in (x64, x86, arm64))
    assert find_ttd_cdb() == x64


def test_find_ttd_cdb_falls_back_to_x86_when_x64_is_absent(monkeypatch):
    x64, x86, arm64 = DEFAULT_CDB_TTD_PATHS
    monkeypatch.setattr(debug_session.os.path, "isfile", lambda p: p in (x86, arm64))
    assert find_ttd_cdb() == x86


def test_find_ttd_cdb_ignores_the_classic_sdk_cdb_even_if_present(monkeypatch):
    """The SDK build rejects a TTD trace outright ("Could not match Dump File
    signature") and exits, so a TTD session must never resolve to it even when
    it exists and sorts first in DEFAULT_CDB_PATHS."""
    sdk_cdb = DEFAULT_CDB_PATHS[0]
    monkeypatch.setattr(debug_session.os.path, "isfile", lambda p: p == sdk_cdb)
    assert find_ttd_cdb() is None
