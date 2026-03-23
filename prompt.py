from langchain_core.prompts import ChatPromptTemplate

outline_prmpt = ChatPromptTemplate.from_messages([
    # System Prompt
    ("system", "You are an expert content strategiest."
    "Return your response as a valid JSON text only"
    "{format_instructions}"),
    # Human Prompt
    ("human", '''Create a blog post outline for the following:
Topic: {topic}
Audience: {audience}
Number of sections: {num_sections}
''')
])

expand_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert blog writer."),
    ("human", '''Given this blog outline:
    Title: {title}
    Sections: {sections}
    Write a full, engaging introdiction paragraph for this blog post.
    Target audience: {audience}
    Keep it to 3-4 sentences
    ''')
])
