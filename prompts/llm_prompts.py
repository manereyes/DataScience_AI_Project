from langchain_core.prompts import FewShotPromptTemplate, PromptTemplate
import json

def sql_retriever_prompt(input: str, table_info: list) -> FewShotPromptTemplate:
    with open('./example/example_queries.json', 'r') as file:
        examples = json.load(file)
        file.close()

    example_prompt = PromptTemplate.from_template(
        "User input: {input}\nSQL query: {query}"
        )
    prompt = FewShotPromptTemplate(
        examples=examples[:5],
        example_prompt=example_prompt,
        prefix="You are a SQLite expert. Given an input question, create a syntactically correct SQLite query to run. Unless otherwise specificed, do not return more than {top_k} rows.\n\nHere is the list of the table names: {table_info}\n\nBelow are a number of examples of questions and their corresponding SQL queries. Return only the SQL query.",
        suffix="User input: {input}\nSQL query: ",
        input_variables=["input", "top_k", "table_info"],
        )
    return prompt.format(input=input, top_k=10, table_info=table_info)

######

#input = "Give me all the information of the order reviews"
#table_info = ['customers', 'geolocation', 'leads_closed', 'leads_qualified', 'order_items', 'order_payments', 'order_reviews', 'orders', 'product_category_name_translation', 'products', 'sellers']

#call = sql_retriever_prompt(input, table_info)
#print(call)