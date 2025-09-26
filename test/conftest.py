# tests/conftest.py
import os

os.environ["PROFILE"] = "test"  # Settings가 import 되기 전에 test 프로필 고정

import time
from uuid import uuid4
from urllib.parse import urlparse

import pytest
from testcontainers.core.generic import DockerContainer
from testcontainers.redis import RedisContainer

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure

REPLSET_NAME = "rs0"


# ------------------------------
# MongoDB replica set 초기화 유틸
# ------------------------------
def _initiate_replset(
    uri_no_rs: str, member_host: str, member_port: int, replset: str
) -> None:
    """
    mongod --replSet <name>로 띄운 뒤 replica set을 초기화.
    - initiate는 호스트에서 실행하되,
    - 멤버 host는 "컨테이너 내부에서 자기 자신에 도달 가능한 주소"를 넣어야 함.
      (단일 노드인 경우 '127.0.0.1:27017' 권장)
    이미 초기화되어 있으면 통과.
    """
    from pymongo import MongoClient as _SyncClient

    client = _SyncClient(
        uri_no_rs, directConnection=True, serverSelectionTimeoutMS=2000
    )

    # mongod ready 대기
    deadline = time.time() + 30
    last_err = None
    while time.time() < deadline:
        try:
            client.admin.command("ping")
            break
        except Exception as e:  # pragma: no cover
            last_err = e
            time.sleep(0.3)
    else:
        raise ConnectionFailure(f"Mongo not ready: {last_err}")

    # 이미 initiated?
    try:
        client.admin.command("replSetGetStatus")
        return
    except Exception:
        pass

    cfg = {
        "_id": replset,
        "members": [{"_id": 0, "host": f"{member_host}:{member_port}"}],
    }
    try:
        client.admin.command("replSetInitiate", cfg)
    except OperationFailure as e:
        msg = str(e)
        if "already initialized" not in msg and "InvalidReplicaSetConfig" not in msg:
            raise

    # PRIMARY 대기
    deadline = time.time() + 40
    while time.time() < deadline:
        try:
            status = client.admin.command("replSetGetStatus")
            if any(
                m.get("state") == 1 or m.get("stateStr") == "PRIMARY"
                for m in status.get("members", [])
            ):
                return
        except Exception:
            pass
        time.sleep(0.5)
    raise TimeoutError("Replica set did not become PRIMARY in time")


# ------------------------------
# Session-scoped infra containers
# ------------------------------
@pytest.fixture(scope="session")
def mongo_url():
    """
    mongo 컨테이너를 replica set 모드로 띄우고 PRIMARY 될 때까지 초기화.
    반환: mongodb://<host>:<published_port>/?replicaSet=rs0  (DB명은 포함 X → DB_NAME으로 분리)
    """
    cmd = "mongod --bind_ip_all --replSet rs0 --port 27017"
    with (
        DockerContainer("mongo:7").with_command(cmd).with_exposed_ports(27017) as mongo
    ):
        host = mongo.get_container_host_ip()  # 호스트 OS 기준 주소 (예: 127.0.0.1)
        port = int(mongo.get_exposed_port(27017))  # 퍼블리시드 포트 (예: 57xxx)

        # initiate 호출은 호스트에서, 멤버 host는 컨테이너 내부 루프백으로 등록해야 함
        #   - initiate 접속 URI  : mongodb://{host}:{port}/   (호스트에서 퍼블리시드 포트로)
        #   - 멤버 등록 host/port: 127.0.0.1:27017           (컨테이너 내부 관점)
        _initiate_replset(f"mongodb://{host}:{port}/", "127.0.0.1", 27017, REPLSET_NAME)

        yield f"mongodb://{host}:{port}/?replicaSet={REPLSET_NAME}"


@pytest.fixture(scope="session")
def redis_url():
    with RedisContainer("redis:7-alpine") as r:
        host = r.get_container_host_ip()
        port = int(r.get_exposed_port(6379))
        yield f"redis://{host}:{port}"


# ------------------------------
# 세션 전체 공통 ENV 주입 (Settings가 읽을 값들)
# ------------------------------
@pytest.fixture(autouse=True, scope="session")
def _inject_env_session(mongo_url, redis_url):
    m = urlparse(mongo_url)
    r = urlparse(redis_url)

    os.environ["MONGO_URI"] = mongo_url
    os.environ["DB_CLUSTER_ENDPOINT"] = m.hostname or "localhost"
    os.environ["DB_PORT"] = str(m.port or 27017)
    os.environ["REDIS_HOST"] = r.hostname or "localhost"
    os.environ["REDIS_PORT"] = str(r.port or 6379)
    os.environ["PROFILE"] = "test"
    # 잘못된 호출 수정
    os.environ.pop("CERT_PATH", None)


# ------------------------------
# Per-test isolation + 전역 싱글톤 재초기화
# ------------------------------
@pytest.fixture(autouse=True)
def _isolate_and_reinit(monkeypatch, mongo_url):
    """
    각 테스트마다:
      1) 전역 싱글톤 close_db()로 리셋
      2) 고유 Mongo DB_NAME, 전용 Redis DB index 환경변수 주입
      3) init_db(Settings()) 로 공통 모듈 재초기화
      4) 테스트 후 Mongo DB drop + Redis flushdb
    """
    from hypurrquant.settings import Settings
    from hypurrquant.db import init_db, close_db
    from hypurrquant.db.redis import get_redis_sync

    # --- 고유 Mongo DB 이름 ---
    dbname = f"testdb_{uuid4().hex[:8]}"
    monkeypatch.setenv("DB_NAME", dbname)

    # --- 전용 Redis DB index (xdist 병렬 고려) ---
    worker = os.getenv("PYTEST_XDIST_WORKER", "gw0")  # gw0, gw1, ...
    try:
        wid = int(worker.replace("gw", ""))
    except ValueError:
        wid = 0
    redis_db_index = min(15, 1 + wid)  # 기본 Redis DB는 0~15
    monkeypatch.setenv("REDIS_DB", str(redis_db_index))

    # --- 전역 클라이언트 재초기화 ---
    close_db()
    init_db(Settings())

    # --- 테스트 실행 ---
    yield

    # --- 정리: Mongo DB drop + Redis flush ---
    try:
        sync_client = MongoClient(mongo_url)
        sync_client.drop_database(dbname)
    except Exception:
        pass
    try:
        get_redis_sync().flushdb()
    except Exception:
        pass
