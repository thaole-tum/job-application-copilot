from app.workflows.application_flow import build_application

if __name__ == "__main__":
    url = input("Job URL: ")
    result = build_application(url)

    print("\n\n===== RESULT =====\n")
    print(result)
