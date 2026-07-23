from atlas.cognitive.process.cognitive_process_engine import CognitiveProcessEngine
from atlas.cognitive.meta_cognition.meta_cognition_engine import MetaCognitionEngine
from atlas.cognitive.workflow.workflow_engine import WorkflowEngine, Workflow, Stage
from atlas.cognitive.process.process import Process


def test_cognitive_process_engine_runs_a_cognitive_workflow():
    workflow_engine = WorkflowEngine()
    workflow_engine.register_workflow(Workflow(
        name='default',
        stages=[
            Stage(name='Understand'),
            Stage(name='Plan'),
        ],
    ))
    process_engine = CognitiveProcessEngine(workflow_engine=workflow_engine)
    process = Process(process_id='P-100', goal={'goal': 'explore'})

    result = process_engine.run(process, workflow_name='default')

    assert result['completed'] is True
    assert result['stages'][0] == 'Understand'
    assert process.context.plan['workflow'] == 'default'


def test_meta_cognition_engine_recommends_replan_when_confidence_is_low():
    engine = MetaCognitionEngine()
    decision = engine.evaluate({'confidence': 0.3, 'risk': 0.8, 'cost': 4})

    assert decision['decision'] == 'replan'
