list1=("Instances" "Similarities" "Scientific")
list2=("CoT" "deep_breath" "few_shot")

# # Accessing elements directly
# echo "First item in list1: ${list1[0]}" # apple
# echo "First item in list2: ${list2[0]}" # dog

# Iterating over both arrays
for dataset in "${list1[@]}"
do
    for prompt in "${list2[@]}"
    do
        # echo $dataset\_$prompt
        python3 single_agent.py -d $dataset -n 100 -t $prompt
    done
done

# for dataset in "${list1[@]}"
# do
#     # echo $dataset\_$prompt
#     echo python3 single_agent.py -d $dataset -n 100 -t basic

# done