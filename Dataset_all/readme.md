# This is the folder for all the augmented dataset
- It contains Scientific Creativity and WKCT dataset.

## The format of each category

### WKCT
- It contains AUT, Instances test and Similarities test.
- Each of them have 10, 30 and 100 .json files
- Format:
    ```
    {
        "Task": [
            {
                "Problem": [
                    ...
                ]
                "Purpose": "Prompt 1"
            },
            ...
            {
                "Problem": [
                    ...
                ]
                "Purpose": "Prompt n"
            },
            ...
        ],
        "Examples": [
            {
                "object": "Fork"
            },
            ...
            {
                "object": "Mirror"
            }
        ],
        "Amount": n
    }
    ```
    
## AUT

## Instances Test

## Similarities Test

### Scientific Creativity Test

