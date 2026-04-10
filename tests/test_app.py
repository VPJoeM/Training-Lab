"""API and route tests -- exercises the full FastAPI app with a test client"""

import json
import pytest
import pytest_asyncio


# ── health check ──

@pytest.mark.asyncio
async def test_health(client):
    resp = await client.get("/health")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "ok"
    assert "timestamp" in data


# ── dashboard routes ──

@pytest.mark.asyncio
async def test_root_redirects_to_baremetal(client):
    resp = await client.get("/", follow_redirects=False)
    assert resp.status_code == 307
    assert "/track/baremetal" in resp.headers["location"]


@pytest.mark.asyncio
async def test_dashboard_renders(client):
    resp = await client.get("/track/baremetal")
    assert resp.status_code == 200
    assert "Test Module" in resp.text
    assert "Scenario Module" in resp.text


@pytest.mark.asyncio
async def test_dashboard_404_bad_track(client):
    resp = await client.get("/track/nonexistent")
    assert resp.status_code == 404


# ── module pages ──

@pytest.mark.asyncio
async def test_module_page_renders(client):
    resp = await client.get("/track/baremetal/module/01-test-module")
    assert resp.status_code == 200
    assert "Test Module" in resp.text
    assert "test lesson" in resp.text.lower()


@pytest.mark.asyncio
async def test_module_page_shows_scripts(client):
    resp = await client.get("/track/baremetal/module/01-test-module")
    assert resp.status_code == 200
    assert "test-script.sh" in resp.text


@pytest.mark.asyncio
async def test_module_page_shows_scenarios(client):
    resp = await client.get("/track/baremetal/module/02-scenario-module")
    assert resp.status_code == 200
    assert "Fix The Thing" in resp.text


@pytest.mark.asyncio
async def test_module_404_bad_module(client):
    resp = await client.get("/track/baremetal/module/99-fake")
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_module_visit_creates_progress(client):
    await client.get("/track/baremetal/module/01-test-module")
    resp = await client.get("/api/progress")
    progress = resp.json()["progress"]
    assert any(p["module"] == "01-test-module" for p in progress)


# ── lesson completion ──

@pytest.mark.asyncio
async def test_complete_lesson(client):
    # visit first to create the row
    await client.get("/track/baremetal/module/01-test-module")
    resp = await client.post("/api/module/baremetal/01-test-module/complete")
    assert resp.status_code == 200
    assert "complete" in resp.text.lower()

    # verify in progress API
    progress = (await client.get("/api/progress")).json()["progress"]
    mod = next(p for p in progress if p["module"] == "01-test-module")
    assert mod["lesson_completed"] == 1
    assert mod["completed_at"] is not None


# ── scenario page ──

@pytest.mark.asyncio
async def test_scenario_page_renders(client):
    resp = await client.get("/track/baremetal/module/02-scenario-module/scenario/fix-the-thing")
    assert resp.status_code == 200
    assert "Fix The Thing" in resp.text
    assert "Something is broken" in resp.text


@pytest.mark.asyncio
async def test_scenario_404_bad_id(client):
    resp = await client.get("/track/baremetal/module/02-scenario-module/scenario/nonexistent")
    assert resp.status_code == 404


# ── terminal page ──

@pytest.mark.asyncio
async def test_terminal_page(client):
    resp = await client.get("/terminal")
    assert resp.status_code == 200
    assert "terminal" in resp.text.lower()


# ── progress API ──

@pytest.mark.asyncio
async def test_progress_api_empty(client):
    resp = await client.get("/api/progress")
    assert resp.status_code == 200
    assert resp.json()["progress"] == []


@pytest.mark.asyncio
async def test_progress_api_after_activity(client):
    await client.get("/track/baremetal/module/01-test-module")
    await client.get("/track/baremetal/module/02-scenario-module")

    resp = await client.get("/api/progress")
    progress = resp.json()["progress"]
    assert len(progress) == 2


# ── teardown-all API ──

@pytest.mark.asyncio
async def test_teardown_all_no_active(client):
    resp = await client.post("/api/scenarios/teardown-all")
    assert resp.status_code == 200
    assert resp.json()["teardowns"] == []


# ── connection test API ──

@pytest.mark.asyncio
async def test_connection_test_endpoint(client):
    """connection test will fail (no real target) but should return a response"""
    resp = await client.get("/api/connection-test")
    assert resp.status_code == 200
    data = resp.json()
    assert "connected" in data
    assert "message" in data
