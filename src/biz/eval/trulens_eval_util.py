from trulens_eval.feedback.provider import OpenAI
from trulens_eval.app import App
from trulens_eval import TruChain, Feedback
import numpy as np

class TrulensEvalUtil:
    """
    Utility class for Trulens evaluation using OpenAI's feedback provider.
    """

    def __init__(self, app_id: str, rag_chain):
        """
        Initializes the TrulensEvalUtil with the given app ID and RAG chain.
        
        Parameters:
        app_id (str): The application ID for the Trulens evaluation.
        rag_chain: The RAG (Retrieval-Augmented Generation) chain used for the evaluation.
        """
        self.app_id = app_id  
        self.rag_chain = rag_chain  
        self.provider = OpenAI()  
        
        self.context = App.select_context(self.rag_chain)  # Select context
        self.f_answer_relevance, self.f_context_relevance, self.f_groundedness = self.get_eval_functions(self.context)  # Get evaluation functions
        
        self.tru_recorder = TruChain(
                self.rag_chain, 
                app_id=self.app_id, 
                feedbacks=[self.f_answer_relevance, self.f_context_relevance, self.f_groundedness]
            )

    def do_evaluation(self, prompt, chat_history):
        """
        Evaluate the given prompt and chat history using the TruChain recorder.
        
        Parameters:
        prompt (str): The input question or prompt to evaluate.
        chat_history (list): The chat history related to the prompt.
        
        Returns:
        tuple: The response from the RAG chain and the evaluation record.
        """
        try:
            tru_response, tru_record = self.tru_recorder.with_record(self.rag_chain.invoke, {"question": prompt, "chat_history": chat_history})
            tru_record.wait_for_feedback_results()
            return tru_response, tru_record
        except Exception as e:
            raise RuntimeError(f"Error during evaluation: {e}")

    def get_eval_functions(self, context):
        """
        Define and return the evaluation functions for groundedness, answer relevance, and context relevance.
        
        Parameters:
        context: The context selected for feedback evaluation.
        
        Returns:
        tuple: The groundedness, answer relevance, and context relevance feedback functions.
        """
        try:
            f_answer_relevance = (
                Feedback(self.provider.relevance)
                .on_input_output()  
            )

            f_context_relevance = (
                Feedback(self.provider.context_relevance_with_cot_reasons)
                .on_input()  
                .on(context)  
                .aggregate(np.mean)  
            )
            
            f_groundedness = (
                Feedback(self.provider.groundedness_measure_with_cot_reasons)
                .on(context.collect())  
                .on_output()  
            )

            return f_answer_relevance, f_context_relevance, f_groundedness
        except Exception as e:
            raise RuntimeError(f"Error in defining evaluation functions: {e}")