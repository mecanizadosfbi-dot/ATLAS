from atlas.runtime.cognitive_runtime import CognitiveRuntime
from atlas.cognitive.inspector.inspector import CognitiveInspector


def test_cognitive_runtime_enqueues_and_runs_processes():
    runtime = CognitiveRuntime()
    runtime.start()
    runtime.enqueue_process('P-001', priority=3, metadata={'goal': 'explore'})
    process_id = runtime.run_next()
    assert process_id == 'P-001'
    assert runtime.scheduler.size() == 0


def test_inspector_tracks_workers_and_snapshot():
    inspector = CognitiveInspector()
    inspector.register_worker('Executive', 'Idle')
    inspector.register_worker('Planning', 'Busy')
    snapshot = inspector.snapshot()
    assert snapshot['workers']['Planning'] == 'Busy'
