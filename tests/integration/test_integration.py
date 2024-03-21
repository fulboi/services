import pytest
from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parent.parent.parent

sys.path.append(str(BASE_DIR))
sys.path.append(str(BASE_DIR / 'student_service/app'))
sys.path.append(str(BASE_DIR / 'teacher_service/app'))

from student_service.app.main import service_alive as student_status
from teacher_service.app.main import service_alive as teacher_status


@pytest.mark.asyncio
async def test_item_service_connection():
    r = await student_status()
    assert r == {'message': 'service alive'}

@pytest.mark.asyncio
async def test_shop_service_connection():
    r = await teacher_status()
    assert r == {'message': 'service alive'}
