from app.agent import ask_agent


question = input("Ask a business question: ")

answer = ask_agent(question)

print("\nAnswer:", answer)