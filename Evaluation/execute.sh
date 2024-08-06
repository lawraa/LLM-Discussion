# for i in {2..8}; do
#     echo python_script.py "discussion_final_results_02-21_02:02:39_2_$i"
# done

# python3 auto_grade_final.py -v 3 -i Scientific_Test_single_basic-10-0 -t sampling -s 3 -d scientific
# python3 auto_grade_final.py -v 3 -i Instances_Test_single_basic-10-0 -t sampling -s 3 -d instances
# python3 auto_grade_final.py -v 3 -i Similarities_Test_single_basic-10-0 -t sampling -s 3 -d similarities

# for ((i=1; i<=3; i+=1))
# do
# 	# time python3 auto_grade.py -v 3 -i discussion_final_results_2024-02-24_10-$i\_final_results -c all -t sampling -s 3 -d aut
# 	# echo auto_grade.py -v 3 -i discussion_2024-02-22_2_6_q$i\_final_results -c all -t sampling -s 3 -d aut
# 	python3 auto_grade.py -v 3 -i discussion_final_results_02-24_10-$i -c all -t sampling -s 3 -d aut
# done

list1=("Instances" "Similarities" "Scientific")
# list1=("Scientific")
list2=("basic" "CoT" "deep_breath" "few_shot")

for dataset in "${list1[@]}"
do
    for prompt in "${list2[@]}"
    do
        # echo $dataset\_$prompt
        python3 auto_grade_final.py -v 3 -i $dataset\_single_$prompt\_100-0 -t sampling -s 3 -d $dataset
    done
done

# # Accessing elements directly
# echo "First item in list1: ${list1[0]}" # apple
# echo "First item in list2: ${list2[0]}" # dog

# python3 auto_grade_final.py -v 3 -i Similarities_Test_single_basic-10-0 -t sampling -s 3 -d similarities
# Iterating over both arrays


# for dataset in "${list1[@]}"
# do
#     # echo $dataset\_$prompt
#     python3 single_agent.py -d $dataset -n 100 -t basic
# done