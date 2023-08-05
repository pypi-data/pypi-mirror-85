import py2neo
import pytest
from py2neo.wiring import WireError

from weaveio.basequery.query import Path
from weaveio.basequery.tests.example_structures.one2one import MyData


@pytest.fixture(scope='session')
def workdir(tmpdir_factory):
    d = tmpdir_factory.mktemp("data")
    for i in range(5):
        fname = Path(str(d.join(f'{i}.fits')))
        with open(str(fname), 'w') as file:
            file.write('')
    return d


@pytest.fixture
def data(workdir):
    return MyData(workdir, port=None)  # set to None for safety


@pytest.fixture(scope='session')
def database(workdir):
    try:
        data = MyData(workdir, port=7687)
        assert data.graph.neograph.name == 'testweaveiodonotuse', "I will not run tests on this database as a safety measure"
        data.graph.neograph.run('MATCH (n) DETACH DELETE n')
    except (AssertionError, WireError):
        pytest.xfail("unsupported configuration of testing database")
    else:
        data.directory_to_neo4j()
        data.validate()
        return data