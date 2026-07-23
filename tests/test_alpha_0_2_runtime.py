from atlas.cognitive.workflow.workflow_engine import WorkflowEngine, Workflow, Stage
from atlas.cognitive.workflow.workflow_context import WorkflowContext
from atlas.cognitive.scheduler.scheduler import CognitiveScheduler
from atlas.cognitive.inspector.inspector import CognitiveInspector
from atlas.core.dispatcher import Dispatcher
from atlas.core.event import Event


def test_workflow_context_tracks_state_machine_progress():
    context = WorkflowContext(workflow_id='wf-1', current_stage='understand')
    context.advance('reasoning')
    assert context.current_stage == 'reasoning'
    assert context.previous_stage == 'understand'
    assert context.history[-1] == 'reasoning'


def test_scheduler_prioritizes_ready_processes():
    scheduler = CognitiveScheduler()
    scheduler.enqueue('P-2', priority=1)
    scheduler.enqueue('P-1', priority=5)
    assert scheduler.next() == 'P-1'


def test_inspector_exposes_inspect_payload():
    inspector = CognitiveInspector()
    inspector.register_process('P-001', workflow='default', stage='planning', thought='T-004', confidence=0.84, events=12, elapsed_ms=183)
    payload = inspector.inspect('P-001')
    assert payload['process'] == 'P-001'
    assert payload['workflow'] == 'default'
    assert payload['stage'] == 'planning'


def test_dispatcher_runs_middleware_chain():
    dispatcher = Dispatcher(kernel=None)

    def validation(event):
        event.metadata['validated'] = True
        return event

    def tracing(event):
        event.metadata['traced'] = True
        return event

    dispatcher.use(validation)
    dispatcher.use(tracing)

    event = Event(event_type='demo')
    dispatcher._run_middleware(event)

    assert event.metadata['validated'] is True
    assert event.metadata['traced'] is True
