from typing import Dict, Union, List

from langchain.callbacks.base import BaseCallbackHandler
from langchain_core.agents import AgentFinish, AgentAction
from langchain_core.messages import BaseMessage
from langchain_core.outputs import LLMResult
from streamlit.runtime.state import SessionStateProxy
from traitlets import Any


class SimpleCallback(BaseCallbackHandler):
    def __init__(self, st_state: SessionStateProxy) -> None:
        """

        Args:
            st_state (SessionStateProxy): session state of the streamlit app

        Returns:
            None 
        """
        super(SimpleCallback, self).__init__()
        self.st_state = st_state

    def on_llm_start(
            self, serialized: Dict[str, Any], prompts: List[str], **kwargs: Any
    ) -> Any:
        """Run when LLM starts running.

        Args:
            serialized (Dict[str, Any]): 
            prompts (List[str]): 
            **kwargs (Any): 

        Returns:
            object (Any): 
        """
        
        return super(SimpleCallback, self).on_llm_start(serialized, prompts, **kwargs)

    def on_chat_model_start(
            self, serialized: Dict[str, Any], messages: List[List[BaseMessage]], **kwargs: Any
    ) -> Any:
        """Run when Chat Model starts running.

        Args:
            serialized (Dict[str, Any]): 
            messages (List[List[BaseMessage]]): 
            **kwargs (Any): 

        Returns:
            object (Any): 
        """
        
        return super(SimpleCallback, self).on_chat_model_start(serialized, messages, **kwargs)

    def on_llm_new_token(self, token: str, **kwargs: Any) -> Any:
        """Run on new LLM token. Only available when streaming is enabled.

        Args:
            token (str): 
            **kwargs (Any): 

        Returns:
            object (Any): 
        """
        
        return super(SimpleCallback, self).on_llm_new_token(token, **kwargs)

    def on_llm_end(self, response: LLMResult, **kwargs: Any) -> Any:
        """Run when LLM ends running.

        Args:
            response (LLMResult): 
            **kwargs (Any): 

        Returns:
            object (Any): 
        """
        
        return super(SimpleCallback, self).on_llm_end(response, **kwargs)

    def on_llm_error(
            self, error: Union[Exception, KeyboardInterrupt], **kwargs: Any
    ) -> Any:
        """Run when LLM errors.

        Args:
            error (Union[Exception, KeyboardInterrupt]):
            **kwargs (Any):

        Returns:
            object (Any):
        """
        
        return super(SimpleCallback, self).on_llm_error(error, **kwargs)

    def on_chain_start(
            self, serialized: Dict[str, Any], inputs: Dict[str, Any], **kwargs: Any
    ) -> Any:
        """Run when chain starts running.

        Args:
            serialized (Dict[str, Any]):
            inputs (Dict[str, Any]):
            **kwargs (Any):

        Returns:
            object (Any):
        """
        
        return super(SimpleCallback, self).on_chain_start(serialized, inputs, **kwargs)

    def on_chain_end(self, outputs: Dict[str, Any], **kwargs: Any) -> Any:
        """Run when chain ends running.

        Args:
            outputs (Dict[str, Any]):
            **kwargs (Any):

        Returns:
            object (Any):
        """
        
        return super(SimpleCallback, self).on_chain_end(outputs, **kwargs)

    def on_chain_error(
            self, error: Union[Exception, KeyboardInterrupt], **kwargs: Any
    ) -> Any:
        """Run when chain errors.

        Args:
            error (Union[Exception, KeyboardInterrupt]):
            **kwargs (Any):

        Returns:
            object (Any):
        """
        
        return super(SimpleCallback, self).on_chain_error(error, **kwargs)

    def on_tool_start(
            self, serialized: Dict[str, Any], input_str: str, **kwargs: Any
    ) -> Any:
        """Run when tool starts running.

        Args:
            serialized (Dict[str, Any]):
            input_str (str):
            **kwargs (Any):

        Returns:
            object (Any):
        """
        
        return super(SimpleCallback, self).on_tool_start(serialized, input_str, **kwargs)

    def on_tool_end(self, output: Any, **kwargs: Any) -> dict | Any:
        """Run when tool ends running.
        Adds geocode_points in streamlit state
        Args:
            output (Any):
            **kwargs (Any):

        Returns:
            object (Any):
        """

        if isinstance(output, dict) and output.get('geocode_points', None) is not None:
            geocode_points = {'geocode_points': output['geocode_points'].copy()}
            self.st_state.messages.append(geocode_points)
            output['geocode_points'] = ""
            return output
        return super(SimpleCallback, self).on_tool_end(output, **kwargs)

    def on_tool_error(
            self, error: Union[Exception, KeyboardInterrupt], **kwargs: Any
    ) -> Any:
        """Run when tool errors.

        Args:
            error (Union[Exception, KeyboardInterrupt]):
            **kwargs (Any):

        Returns:
            object (Any):
        """

        return super(SimpleCallback, self).on_tool_error(error, **kwargs)

    def on_text(self, text: str, **kwargs: Any) -> Any:
        """Run on arbitrary text.

        Args:
            text (str):
            **kwargs (Any):

        Returns:
            object (Any):
        """
        
        return super(SimpleCallback, self).on_text(text, **kwargs)

    def on_agent_action(self, action: AgentAction, **kwargs: Any) -> Any:
        """Run on agent action.

        Args:
            action (AgentAction):
            **kwargs (Any):

        Returns:
            object (Any):
        """
        
        return super(SimpleCallback, self).on_agent_action(action, **kwargs)

    def on_agent_finish(self, finish: AgentFinish, **kwargs: Any) -> Any:
        """Run on agent end.

        Args:
            finish (AgentFinish):
            **kwargs (Any):

        Returns:
            object (Any):
        """
        
        return super(SimpleCallback, self).on_agent_finish(finish, **kwargs)
