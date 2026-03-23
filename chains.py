from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser, PydanticOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableParallel, RunnableLambda
from dotenv import load_dotenv
from prompt import outline_prmpt, expand_prompt
from schema import BlogOutline

load_dotenv()

def build_pipeline():
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.9)
    parser = PydanticOutputParser(pydantic_object=BlogOutline)

    # Step 1: Get format instructions from the parser
    step1_add_format = RunnablePassthrough.assign(
        format_instructions = RunnableLambda(
            lambda x : parser.get_format_instructions()
        )
    )
    # This will add a new key "format_instructions" to the input of the outline prompt

    # Step 2: Add that format instructions to the outline prompt
    step2_add_outline = RunnablePassthrough.assign(
        outline = outline_prmpt | llm | parser
    )
    # That format instructions will be used by the outline prompt.
    # The output of this step will have a new key "outline"

    # Step 3: Extract the relevant input for the expand_prompt from the output we received in outline
    step3_reshape = RunnableLambda(
        lambda x : {
            "title": x['outline'].title,
            'sections': ", ".join(x["outline"].sections),
            "audience": x["audience"]
        }
    )
    # This will reshape the output of step 2 to match the input expected by the expand prompt
    
    # Step 4: Chain2 expands the outline into an intro paragraph 
    step4_expand = expand_prompt | llm | StrOutputParser()
    # This will take the reshaped output from step 3, feed it into the expand prompt, and then parse the final output as a string (the intro paragraph)

    # Final chain = pass everything in each other
    full_pipeline = step1_add_format | step2_add_outline | step3_reshape | step4_expand
    # This will run all the steps in sequence, passing the output of one step as the input to the next step.

    return parser, full_pipeline
