from atlas.cognitive.process.process_manager import ProcessManager
from atlas.cognitive.workflow.workflow_engine import WorkflowEngine, Workflow, Stage, Transition
from atlas.cognitive.inspector.inspector import CognitiveInspector


def test_workflow_engine_runs_configurable_pipeline():
    engine = WorkflowEngine()
    workflow = Workflow(
        name='goal_pipeline',
        stages=[
            Stage(name='Understand', executor=lambda ctx: ctx.update({'stage': 'Understand'})),
            Stage(name='Planning', executor=lambda ctx: ctx.update({'stage': 'Planning'})),
            Stage(name='Completed', executor=lambda ctx: ctx.update({'stage': 'Completed'})),
        ],
    )
    engine.register_workflow(workflow)

    process = ProcessManager().create_process({'goal': 'explore'})
    result = engine.execute(process, workflow.name)

    assert result['completed'] is True
    assert result['stages'] == ['Understand', 'Planning', 'Completed']
    assert process.context.plan is not None


def test_inspector_reports_snapshot():
    inspector = CognitiveInspector()
    inspector.record_event('Executive', 'goal received')
    inspector.record_event('Planning', 'plan created')

    snapshot = inspector.snapshot()

    assert snapshot['events'] >= 2
    assert snapshot['current_stage'] == 'Planning'
    assert snapshot['active_process'] is None
