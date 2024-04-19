from abc import ABC, abstractmethod
from typing import Union

from langchain import hub
from langchain.agents import AgentExecutor, create_react_agent
from langchain.agents import AgentType
from langchain.memory.chat_memory import BaseChatMemory
from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.language_models import BaseLLM, BaseChatModel
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import BaseTool


class TravelAgent(ABC):

    # components of chatbot - llm, memory, template, tools, prompt, response

    @abstractmethod
    def __init__(self, llm: Union[BaseLLM, BaseChatModel], memory: BaseChatMemory, agent_type: AgentType,
                 verbose: bool) -> None:
        """
        Abstract class for travel chat agent
        Args:
            llm (Union[BaseLLM, BaseChatModel]): large language model/chat model for the agent
            memory (BaseChatMemory): memory for the agent
            agent_type (AgentType): AgentType defines the type of agent
            verbose (verbose): verbosity of agent

        Returns:
            None
        """
        self.llm = llm
        self.memory = memory
        self.agent_type = agent_type
        self.tools = []
        self.verbose = verbose
        self.prompt = None

    @abstractmethod
    def get_memory_prompt_template(self) -> None:
        """
        This abstract method enforces a method that returns existing memory prompt template.

        Returns:
            None

        """
        pass

    @abstractmethod
    def set_memory_prompt_template(self, template: str) -> None:
        """
        This abstract method enforces a method that sets the memory prompt template.

        Args:
            template (str): new memory prompt template

        Returns:
            None
        """
        pass

    @abstractmethod
    def get_agent_prompt_template(self) -> None:
        """
        This abstract method enforces a method that returns existing agent prompt template.
        
        Returns:
            None

        """
        pass

    @abstractmethod
    def set_agent_prompt_template(self, template: str) -> None:
        """
        This abstract method enforces a method that sets the agent prompt template
        
        Args:
            template (str): new agent prompt template

        Returns:
            None 
        """
        pass

    @abstractmethod
    def make_request(self, prompt: str) -> None:
        """
        This abstract method enforces a method that creates a request to the agent and returns the completion.
        
        Args:
            prompt (object): 

        Returns:
            None
        """
        pass

    @abstractmethod
    def add_tool(self, tool: BaseTool):
        """
        Adds a tool to agent
        Args:
            tool (BaseTool):

        Returns:
            None

        """
        pass

    @abstractmethod
    def clear_memory(self) -> None:
        """
        This abstract method enforces creation of method that clears memory

        Returns:
            None
        """
        pass


class OpenAIAgent(TravelAgent):
    def __init__(self, llm: Union[BaseLLM, BaseChatModel], memory: BaseChatMemory, agent_type: AgentType, verbose: bool,
                 callback: BaseCallbackHandler) -> None:
        """
        OpenAI Travel chat agent
        Args:
            llm (Union[BaseLLM, BaseChatModel]):
            memory (BaseChatMemory):
            agent_type (AgentType):
            verbose (bool):
            callback (str):
        """
        super().__init__(llm, memory, agent_type, verbose)
        self.prompt = hub.pull("hwchase17/react-chat")
        self.callback = callback

    def get_memory_prompt_template(self) -> str:
        """
        Returns the existing prompt template of memory of agent

        Returns:
            template (str):

        """
        return self.memory.prompt.template

    def set_memory_prompt_template(self, template: str) -> None:
        """
        Modifies prompt template of memory of agent
        Args:
            template (str):

        Returns:
            object:
        """
        self.memory.prompt.template = template

    def get_agent_prompt_template(self) -> PromptTemplate:
        """
        Returns the existing prompt template of agent

        Returns:
            template (str):

        """
        return self.prompt

    def set_agent_prompt_template(self, template) -> None:
        """
        Modifies prompt template of agent

        Args:
            template (str):

        Returns:
            object:
        """
        self.prompt = template

    def make_request(self, prompt: str) -> str:
        """
        Makes a call to the agent and returns the output completion

        Args:
            prompt (str):

        Returns:
            response (str):

        """
        agent = create_react_agent(tools=self.tools, llm=self.llm, prompt=self.prompt)
        agent_executor = AgentExecutor(agent=agent, tools=self.tools, verbose=self.verbose, memory=self.memory,
                                       handle_parsing_errors=True)
        input_dict = {"input": prompt}
        input_dict.update(self.memory.load_memory_variables({}))
        print(input_dict)
        response = agent_executor.invoke(input_dict, {"callbacks": [self.callback]})['output']
        return response

    def add_tool(self, tool: BaseTool):
        """
        Adds a tool to the openai chat agent
        Args:
            tool (BaseTool):

        Returns:
            None

        """
        self.tools.append(tool)

    def clear_memory(self) -> None:
        """
        Clears the memory of the agent

        Returns:
            None

        """
        self.memory.clear()
