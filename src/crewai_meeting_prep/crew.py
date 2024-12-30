from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai_meeting_prep.tools.ExaSearchTool import ExaSearchTool

from dotenv import load_dotenv
# load environment variables from .env file
load_dotenv()

openai_llm = LLM(
	model="gpt-4"
)

# If you want to run a snippet of code before or after the crew starts, 
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class CrewaiMeetingPrep():
	"""CrewaiMeetingPrep crew"""

	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	@agent
	def researcher(self) -> Agent:
		return Agent(
			config=self.agents_config['researcher'],
			verbose=True,
			tools=ExaSearchTool.tools(),
			llm=openai_llm
		)

	@agent
	def industry_analyst(self) -> Agent:
		return Agent(
			config=self.agents_config['industry_analyst'],
			verbose=True,
			tools=ExaSearchTool.tools(),
			llm=openai_llm
		)
	
	@agent
	def meeting_strategy_advisor(self) -> Agent:
		return Agent(
			config=self.agents_config['meeting_strategy_advisor'],
			verbose=True,
			tools=ExaSearchTool.tools(),
			llm=openai_llm
		)
	
	@agent
	def briefing_coordinator(self) -> Agent:
		return Agent(
			config=self.agents_config['briefing_coordinator'],
			verbose=True,
			tools=ExaSearchTool.tools(),
			llm=openai_llm
		)

	# To learn more about structured task outputs, 
	# task dependencies, and task callbacks, check out the documentation:
	# https://docs.crewai.com/concepts/tasks#overview-of-a-task
	@task
	def research_task(self) -> Task:
		return Task(
			config=self.tasks_config['research_task'],
			output_file='debug/research.md'
		)

	@task
	def industry_analysis_task(self) -> Task:
		return Task(
			config=self.tasks_config['industry_analysis_task'],
			output_file='debug/industry_analysis.md'
		)
	
	@task
	def meeting_strategy_task(self) -> Task:
		return Task(
			config=self.tasks_config['meeting_strategy_task'],
			output_file='debug/meeting_strategy.md'
		)
	
	@task
	def summary_and_briefing_task(self) -> Task:
		return Task(
			config=self.tasks_config['summary_and_briefing_task'],
			output_file='debug/summary_and_briefing.md'
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the CrewaiMeetingPrep crew"""
		# To learn how to add knowledge sources to your crew, check out the documentation:
		# https://docs.crewai.com/concepts/knowledge#what-is-knowledge

		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
			llm=openai_llm
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)
