import threading

from atlas.core.event import Event
from atlas.kernel.kernel import AtlasKernel
from atlas.modules.orchestrator import Orchestrator


class RecordingKernel:
    def __init__(self):
        self.subscriptions = {}
        self.published = []
        self.timeline = []

    def subscribe(self, topic, callback):
        self.subscriptions.setdefault(topic, []).append(callback)

    def publish(self, topic, payload=None):
        self.published.append((topic, payload))

    def record_cognitive_event(self, stage, detail, event=None, process_id=None, thought_id=None):
        self.timeline.append((stage, detail, event))


class RecordingOrchestrator(Orchestrator):
    def __init__(self):
        super().__init__('Orchestrator')
        self.monitor_calls = []
        self.reflect_calls = []

    def monitor(self, result):
        self.monitor_calls.append(result)

    def reflect(self, result):
        self.reflect_calls.append(result)


def test_orchestrator_waits_for_plan_event_before_monitoring():
    kernel = RecordingKernel()
    orchestrator = RecordingOrchestrator()
    orchestrator.kernel = kernel
    orchestrator.initialize()

    orchestrator.on_memory_found(Event(event_type='memory/found', payload={'memories': ['fact_about_goal']}))

    assert orchestrator.state == 'WAITING'
    assert orchestrator.monitor_calls == []

    orchestrator.on_plan_created(Event(event_type='plan/created', payload={'plan': 'p1'}))

    assert orchestrator.state == 'READY'
    assert len(orchestrator.monitor_calls) == 1
    assert len(orchestrator.reflect_calls) == 1


def test_stop_all_skips_current_thread_when_joining():
    kernel = AtlasKernel()
    kernel._service_threads = {'self': threading.current_thread()}

    kernel.stop_all()

    assert kernel._running is False
