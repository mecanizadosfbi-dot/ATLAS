from atlas.runtime.cognitive_runtime import CognitiveRuntime
from atlas.cognitive.blackboard.blackboard import Blackboard
from atlas.cognitive.inspector.inspector import CognitiveInspector
from atlas.core.decision.decision_engine import DecisionEngine


def test_runtime_registers_workers_and_blackboard_context():
    runtime = CognitiveRuntime()
    runtime.submit_goal({'goal': 'explore'}, priority=2)
    runtime.scheduler.register_worker('worker-1', 'IDLE')
    runtime.scheduler.register_worker('worker-2', 'BUSY')

    assert runtime.scheduler.worker_count() == 2
    assert runtime.scheduler.active_workers() == 1
    assert runtime.blackboard.read_latest(runtime.submit_goal.__self__.process_manager.get(list(runtime.process_manager._processes.keys())[0]).process_id, 'waiting_processes')['priority'] == 2


def test_inspector_snapshot_contains_timeline_and_metrics():
    inspector = CognitiveInspector()
    inspector.record_event('UNDERSTAND', 'received goal')
    inspector.register_process('P-1', workflow='default', stage='Running')
    snapshot = inspector.snapshot()

    assert snapshot['metrics']['events'] == 1
    assert snapshot['timeline'][-1]['stage'] == 'UNDERSTAND'


def test_decision_engine_generates_and_ranks_options():
    engine = DecisionEngine()
    options = engine.generate_options({'goal': 'explore'})
    assert len(options) == 3
    assert options[0]['name'] == 'explore_more'
