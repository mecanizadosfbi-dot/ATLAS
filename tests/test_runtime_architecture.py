from atlas.runtime.cognitive_runtime import CognitiveRuntime


def test_runtime_submits_goal_and_executes_workflow():
    runtime = CognitiveRuntime()
    runtime.start()

    result = runtime.submit_goal({'goal': 'explore'}, priority=4)

    assert result['process_id']
    assert result['thought_id']
    assert runtime.scheduler.size() == 1

    executed = runtime.run_next(workflow_name='default')
    assert executed == result['process_id']
    assert runtime.process_manager.get(result['process_id']).state.name == 'RUNNING'


def test_scheduler_can_pause_and_resume_processes():
    runtime = CognitiveRuntime()
    runtime.submit_goal({'goal': 'plan'}, priority=1)
    runtime.submit_goal({'goal': 'act'}, priority=2)

    runtime.scheduler.pause('P-001')
    assert runtime.scheduler.next() == 'P-002'

    runtime.scheduler.resume('P-001')
    assert runtime.scheduler.next() == 'P-001'
