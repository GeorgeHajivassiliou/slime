import pytest
import numpy as np
import objects
import base

TEST_CASES =[
    pytest.param({"size":1,"expected":["hey"]}),
    pytest.param({"size":2,"expected":["hey","bar"]})
]

@pytest.fixture(params=TEST_CASES)
def test_case(request):
    return request.param

@pytest.fixture
def size(test_case):
    return test_case["size"]
@pytest.fixture
def expected(test_case):
    return test_case["expected"]

@pytest.fixture
def store(size):
    result =    objects.LimitedStore(size)
    return result

def test_get(store,expected):
    store.add("foo")
    store.add("bar")
    store.add("hey")
    observed = store.get()
    assert observed == expected




class TestAgent:

    @pytest.fixture
    def agents(self):
        centres = [(0,0),(2,2),(1,1)]
        velocity = base.Vector(np.array([0,2]))
        centres = [base.Vector(np.array(c)) for c in centres]
        factory = objects.FixedVelocityAgentFactory(velocity)
        result = list(objects.make_n_agents(len(centres),centres,factory))
        return result

    def test_sense(self,agents):

        expected = agents[2]
        observed = agents[0].sense(agents)
        assert observed == expected

    def test_turn(self,agents):
        acting_agent =  agents[0]
        acting_agent.turn(agents[1].position,0)
        observed = acting_agent.velocity

        assert tuple(observed) == (0,2)


def test_measure_angle():
    v1 = base.Vector(np.array([3,4])) # using pythagorean numbers so that result is integer
    v2 = base.Vector(np.array([3,4]))
    expected = 1
    observed = objects.measure_cos_theta(v1,v2)
    assert observed == expected


