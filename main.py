from chains import build_pipeline

def main():
    print("------------------Content Generator------------------")

    topic = input("Enter a topic: ").strip()
    audience = input("Enter the target audience: ").strip()
    num_sections = input("Enter the number of sections: ").strip()

    parser, full_pipeline = build_pipeline()

    # Run chain1 alone to show the outline
    from langchain_core.runnables import RunnablePassthrough, RunnableLambda
    from langchain_openai import ChatOpenAI
    from prompt import outline_prmpt

    print("\n------- Step 1: Generate Blog Outline -------\n")
    outline_chain = (
        RunnablePassthrough.assign(
            format_instructions = RunnableLambda(
                lambda x : parser.get_format_instructions()
            )
        )
        | outline_prmpt
        | ChatOpenAI(model="gpt-4o-mini", temperature=0.7)
        | parser
    )

    outline = outline_chain.invoke({
        "topic": topic,
        "audience": audience,
        "num_sections": num_sections
    })

    print(f"Title: {outline.title}")
    print(f"Intro: {outline.intro}")
    print("Number of sections:")
    for i, sections in enumerate(outline.sections, 1):
        print(f"  Section {i}: {sections}")

    # Run the full pipeline to show the complete blog post
    print("\n------- Step 2: Generate Full Blog Post -------\n")
    result = full_pipeline.invoke({
        "topic": topic,
        "audience": audience,
        "num_sections": num_sections
    }) 
    print(result)

if __name__ == "__main__":
    main()
