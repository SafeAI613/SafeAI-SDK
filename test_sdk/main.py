from safeai import SafeAI


def main():
    evaluator = SafeAI(profile_id="69add18e588e9d005a875804")
    evaluator.initialize()
    
    my_prompt = "אני רוצה להתחתן."
    result = evaluator.evaluate(my_prompt)
    print("Evaluation result:", result)
    
    print(evaluator)
    print("Hello from test-sdk!")


if __name__ == "__main__":
    main()
