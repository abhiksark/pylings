#!/bin/bash

# Define colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'


# Define paths to exercise directories and test directories
EXERCISES_DIR="./exercises"
TESTS_DIR="./tests"

# Get list of exercise files (excluding __init__.py files)
EXERCISE_FILES=$(find "$EXERCISES_DIR" -name "*.py" ! -name "__init__.py")
echo "Running tests for the following exercises:"

# Iterate over exercise files and run tests for each one
for EXERCISE_FILE in $EXERCISE_FILES; do
    # Get the relative path of the exercise file
    EXERCISE_REL_PATH=${EXERCISE_FILE#"$EXERCISES_DIR/"}
    echo "$EXERCISE_REL_PATH"
    
    # Replace the exercise file name with the test file name
    TEST_FILE_REL_PATH=${EXERCISE_REL_PATH/%.py/"_test.py"}

    # Construct the full path of the test file
    TEST_FILE="$TESTS_DIR/$TEST_FILE_REL_PATH"

    if [ -f "$TEST_FILE" ]; then
        printf "Running tests for $EXERCISE_REL_PATH...\n"
        pytest "$TEST_FILE"
        if [ $? -eq 0 ]; then
            printf "${GREEN}All tests passed!${NC}\n\n"
        else
            printf "${RED}Some tests failed.${NC}\n\n"
            exit 1 # Exit with non-zero code on test failure
        fi
    fi
done
