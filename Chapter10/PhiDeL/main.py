import gradio as gr
from langchain.llms import LlamaCpp
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate


def initialize_llm_model(model_path: str = "/Users/ashish.jha/code/personal/MedEL/mistral-7b-openorca.Q4_0.gguf") -> LlamaCpp:
    llm = LlamaCpp(model_path=model_path,
                   n_gpu_layers=1,
                   n_batch=512,
                   n_ctx=2048,
                   f16_kv=True,
                   callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]),
                   temperature=0)
    return llm


# create a global LLM model
llm = initialize_llm_model()


def prepare_answer(input_text: str) -> str:
    prompt = PromptTemplate(
        input_variables=["question"],
        template="""{input_text}\n{question}""")
    llm_chain = LLMChain(prompt=prompt, llm=llm)
    question = "Is this a phishing email (yes or no)? Explain in a few sentences."
    answer = llm_chain.run({"input_text": input_text, "question": question})
    return answer.strip()


iface = gr.Interface(
    fn=prepare_answer,
    inputs=gr.Textbox(label="Paste text (email) here", max_lines=100),
    outputs=[
        gr.Textbox(label="Is this phishing?"),
    ],
    title="PhiDeL",
    description="Phishing Detection using LLM"
)

iface.launch(server_name="0.0.0.0", server_port=8082)
