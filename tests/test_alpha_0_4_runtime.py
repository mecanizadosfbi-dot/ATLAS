from atlas.cognitive.blackboard.blackboard import Blackboard
from atlas.cognitive.inspector.inspector import CognitiveInspector
from atlas.core.decision.decision_engine import DecisionEngine


def test_blackboard_supports_thought_scoped_workspace_entries():
    blackboard = Blackboard()
    blackboard.write('T-001', 'current_hypothesis', {'text': 'candidate'})
    blackboard.write('T-001', 'confidence', {'value': 0.82})

    assert blackboard.read_latest('T-001', 'current_hypothesis')['text'] == 'candidate'
    assert blackboard.context('T-001')['confidence']['value'] == 0.82


def test_decision_engine_scores_and_ranks_options():
    engine = DecisionEngine()
    options = engine.generate_options({'goal': 'explore'})
    ranked = engine.rank()

    assert len(options) == 3
    assert ranked[0]['name'] == 'explore_more'
    assert ranked[0]['score'] >= ranked[-1]['score']


def test_inspector_snapshot_exposes_live_summary():
    inspector = CognitiveInspector()
    inspector.record_event('EVALUATE', 'scoring plan')
    inspector.register_process('P-1', workflow='default', stage='Evaluate')
    snapshot = inspector.snapshot()

    assert snapshot['summary']['running_thoughts'] >= 0
    assert snapshot['current_stage'] == 'EVALUATE'
