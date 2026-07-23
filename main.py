from atlas.kernel.kernel import AtlasKernel
from atlas.modules.executive import ExecutiveCortex
from atlas.modules.orchestrator import Orchestrator
from atlas.modules.memory import Memory
from atlas.modules.reasoning import Reasoning
from atlas.modules.planning import Planning
from atlas.modules.action import Action
from atlas.modules.learning import Learning
from atlas.modules.reflection import Reflection
from atlas.modules.knowledge_graph import KnowledgeGraph
from atlas.modules.tool_ecosystem import ToolEcosystem


def main():
	k = AtlasKernel()
	# Registrar orquestador (director de orquesta)
	k.register(Orchestrator('Orchestrator'))
	# Registros centrales: ProcessManager, ThoughtManager, Blackboard, CapabilityRegistry
	from atlas.cognitive.process.process_manager import ProcessManager
	from atlas.cognitive.thought.thought_manager import ThoughtManager
	from atlas.cognitive.blackboard.blackboard import Blackboard
	from atlas.core.registry.capability_registry import CapabilityRegistry

	process_manager = ProcessManager()
	thought_manager = ThoughtManager()
	blackboard = Blackboard()
	capability_registry = CapabilityRegistry()

	# Exponer en kernel para que los Cortex puedan acceder (poco acoplado)
	k.process_manager = process_manager
	k.thought_manager = thought_manager
	k.blackboard = blackboard
	k.capability_registry = capability_registry
	# Registrar módulos principales
	k.register(ExecutiveCortex('Executive'))
	k.register(Memory('Memory'))
	k.register(Reasoning('Reasoning'))
	k.register(Planning('Planning'))
	k.register(Action('Action'))
	k.register(Learning('Learning'))
	k.register(Reflection('Reflection'))
	k.register(KnowledgeGraph('KnowledgeGraph'))
	k.register(ToolEcosystem('ToolEcosystem'))

	k.initialize_all()
	k.start_all()


if __name__ == '__main__':
	main()
