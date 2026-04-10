"""tests for the SQLite progress/scenario models"""

import json
import pytest
import pytest_asyncio
from app.models import (
    init_db,
    get_progress,
    update_progress,
    get_scenario_state,
    update_scenario_state,
    get_active_scenarios,
    clear_all_progress,
)


@pytest_asyncio.fixture
async def db(temp_db):
    await init_db(temp_db)
    yield temp_db


# ── progress tracking ──

@pytest.mark.asyncio
async def test_empty_progress(db):
    result = await get_progress()
    assert result == []


@pytest.mark.asyncio
async def test_create_progress(db):
    await update_progress("baremetal", "01-env", lesson_completed=0)
    rows = await get_progress("baremetal")
    assert len(rows) == 1
    assert rows[0]["track"] == "baremetal"
    assert rows[0]["module"] == "01-env"
    assert rows[0]["lesson_completed"] == 0
    assert rows[0]["started_at"] is not None


@pytest.mark.asyncio
async def test_update_progress_upsert(db):
    """second call with same track+module should update, not duplicate"""
    await update_progress("baremetal", "01-env", lesson_completed=0)
    await update_progress("baremetal", "01-env", lesson_completed=1)
    rows = await get_progress("baremetal")
    assert len(rows) == 1
    assert rows[0]["lesson_completed"] == 1


@pytest.mark.asyncio
async def test_progress_filter_by_track(db):
    await update_progress("baremetal", "01-env", lesson_completed=0)
    await update_progress("k8s", "01-basics", lesson_completed=0)

    bm = await get_progress("baremetal")
    k8s = await get_progress("k8s")
    all_progress = await get_progress()

    assert len(bm) == 1
    assert len(k8s) == 1
    assert len(all_progress) == 2


@pytest.mark.asyncio
async def test_scenario_completion_tracking(db):
    await update_progress("baremetal", "02-logs", lesson_completed=0)
    completed = json.dumps(["collect-logs", "diagnose-xid"])
    await update_progress("baremetal", "02-logs", scenarios_completed=completed)

    rows = await get_progress("baremetal")
    assert json.loads(rows[0]["scenarios_completed"]) == ["collect-logs", "diagnose-xid"]


# ── scenario state ──

@pytest.mark.asyncio
async def test_scenario_state_default(db):
    result = await get_scenario_state("nonexistent")
    assert result is None


@pytest.mark.asyncio
async def test_scenario_state_lifecycle(db):
    # start
    await update_scenario_state(
        "fix-ecc", track="baremetal", module="03-gpu",
        status="active", started_at="2026-04-09T12:00:00"
    )
    state = await get_scenario_state("fix-ecc")
    assert state["status"] == "active"
    assert state["attempts"] == 0

    # failed attempt
    await update_scenario_state("fix-ecc", attempts=1)
    state = await get_scenario_state("fix-ecc")
    assert state["attempts"] == 1
    assert state["status"] == "active"

    # passed
    await update_scenario_state("fix-ecc", status="passed", completed_at="2026-04-09T12:05:00")
    state = await get_scenario_state("fix-ecc")
    assert state["status"] == "passed"
    assert state["completed_at"] is not None


@pytest.mark.asyncio
async def test_active_scenarios(db):
    await update_scenario_state("sc-1", track="bm", module="01", status="active")
    await update_scenario_state("sc-2", track="bm", module="02", status="active")
    await update_scenario_state("sc-3", track="bm", module="03", status="passed")

    active = await get_active_scenarios()
    assert len(active) == 2
    ids = [s["scenario_id"] for s in active]
    assert "sc-1" in ids
    assert "sc-2" in ids
    assert "sc-3" not in ids


# ── reset ──

@pytest.mark.asyncio
async def test_clear_all_progress(db):
    await update_progress("baremetal", "01-env", lesson_completed=1)
    await update_scenario_state("sc-1", track="bm", module="01", status="active")

    await clear_all_progress()

    assert await get_progress() == []
    assert await get_active_scenarios() == []
