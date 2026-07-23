from atlas.cognitive.thought.thought import Thought
from atlas.cognitive.thought.thought_state import ThoughtState


def test_thought_state_machine_supports_transitions_and_pause_resume():
    thought = Thought(process_id='P-1', goal={'goal': 'plan'})

    thought.transition(ThoughtState.UNDERSTANDING)
    assert thought.state == ThoughtState.UNDERSTANDING

    thought.pause()
    assert thought.state == ThoughtState.CANCELLED

    thought.resume()
    assert thought.state == ThoughtState.UNDERSTANDING
