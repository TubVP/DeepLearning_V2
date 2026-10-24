import os
import sys
import argparse
import json

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--source_code_file", type=str, required=True)
    parser.add_argument("--test_cases", type=str, required=True)
    args = parser.parse_args()

    source_code_file = args.source_code_file
    test_cases = args.test_cases
    
    # read the source code
    with open(source_code_file, "r") as f:
        source_code = f.read()
    
    passed_test_cases = 0
    failed_test_cases = 0
    # read the test cases, convert the content to variables
    with open(test_cases, "r") as f:
        test_cases_data = json.load(f)
    for i, test_case in enumerate(test_cases_data["test_cases"]):
        parameters = test_case["parameters"]
        expected_output = test_case["expected_output"]
        # execute the source code in a namespace
        namespace = {}
        exec(source_code, namespace)
        func = namespace[test_cases_data["function_name"]]  # the function to be tested 
        output = func(**parameters)
        if output == expected_output:
            print(f"Test case {i} passed")
            passed_test_cases += 1
        else:
            print(f"Test case {i} failed")
            print(f"Expected output: {expected_output}")
            print(f"Actual output: {output}")
            failed_test_cases += 1
    
    print("--------------------------------")
    print(f"Total test cases: {len(test_cases_data["test_cases"])}")
    print(f"Passed test cases: {passed_test_cases}/{len(test_cases_data["test_cases"])} ({passed_test_cases / len(test_cases_data["test_cases"]) * 100}%)")
    print(f"Failed test cases: {failed_test_cases}/{len(test_cases_data["test_cases"])} ({failed_test_cases / len(test_cases_data["test_cases"]) * 100}%)")
    print(f"Score: {passed_test_cases / len(test_cases_data["test_cases"]) * 100}%")
    print("--------------------------------")