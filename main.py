from app.agent import ask_agent


company_id = "company_a"

question = input("Ask a business question: ")
answer = ask_agent(company_id, question)
print("\nAnswer:", answer)