from atlas.cognition.memory.memory_store import HierarchicalMemory
from atlas.cognition.scheduler.scheduler import CognitiveScheduler
from atlas.core.decision.decision_engine import DecisionEngine
from atlas.runtime.runtime_manager import RuntimeManager
from atlas.cognitive.blackboard.blackboard import Blackboard
from atlas.cognitive.workflow.workflow_engine import WorkflowEngine, Workflow, Stage
from atlas.cognitive.workflow.workflow_context import WorkflowContext


def test_scheduler_prioritizes_and_retries():
    scheduler = CognitiveScheduler()
    scheduler.enqueue('P-001', priority=1)
    scheduler.enqueue('P-002', priority=5)
    assert scheduler.next() == 'P-002'
    scheduler.mark_retry('P-001')
    assert scheduler.retry_count('P-001') == 1


def test_hierarchical_memory_stores_by_level():
    memory = HierarchicalMemory()
    memory.write('working', {'goal': 'explore'})
    memory.write('semantic', {'concept': 'atlas'})
    assert memory.retrieve('working')[0]['goal'] == 'explore'
    assert memory.retrieve('semantic')[0]['concept'] == 'atlas'


def test_decision_engine_selects_best_option():
    engine = DecisionEngine()
    engine.add_option({'name': 'plan_a', 'confidence': 0.5})
    engine.add_option({'name': 'plan_b', 'confidence': 0.9})
    assert engine.select()['name'] == 'plan_b'


def test_runtime_manager_registers_workers():
    runtime = RuntimeManager()
    worker = runtime.register_worker('Dispatcher')
    assert worker.name == 'Dispatcher'
    assert runtime.get_worker('Dispatcher').name == 'Dispatcher'


def test_blackboard_exposes_stats_api():
    blackboard = Blackboard()
    blackboard.write('thoughts', {'id': 'T-001'})
    blackboard.write('waiting_processes', {'id': 'P-001'})
    blackboard.write('last_tool', {'name': 'search'})
    stats = blackboard.stats()
    assert stats['active_thoughts'] == 1
    assert stats['waiting_processes'] == 1


def test_workflow_engine_uses_explicit_state_context():
    engine = WorkflowEngine()
    workflow = Workflow(
        name='default',
        stages=[Stage(name='Understand'), Stage(name='Planning')],
    )
    engine.register_workflow(workflow)
    context = engine.create_context('wf-1', 'Understand')
    context.advance('Planning')
    assert context.current_stage == 'Planning'
