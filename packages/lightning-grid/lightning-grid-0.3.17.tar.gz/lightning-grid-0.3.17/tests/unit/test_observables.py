from tests.mock_backend import GridAIBackenedTestServer
from grid.observables import style_status, BaseObservable
import grid.client as grid


def monkey_patch_client(self):
    self.client = GridAIBackenedTestServer()


grid.Grid._init_client = monkey_patch_client
GRID = grid.Grid(load_local_credentials=False)
GRID._init_client()
grid.gql = lambda x: x


def test_style_status():
    value = 'test'
    result = style_status(format_string=value, status='running')
    assert '\x1b[33m' in result
    assert value in result

    result = style_status(format_string=value, status='failed')
    assert '\x1b[31m' in result
    assert value in result

    result = style_status(format_string=value, status='finished')
    assert '\x1b[32m' in result
    assert value in result

    result = style_status(format_string=value, status='cancelled')
    assert '\x1b[37m' in result
    assert value in result


def test_get_task_run_dependencies(monkeypatch):
    observable = BaseObservable(client=GRID.client)
    observable._get_task_run_dependencies(run_id='test')
