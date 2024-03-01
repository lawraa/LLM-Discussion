# for i in {2..8}; do
#     echo python_script.py "discussion_final_results_02-21_02:02:39_2_$i"
# done

python3 auto_grade.py -v 3 -i discussion_final_results_02-24_30 -c all -t sampling -s 3 -d aut

for ((i=1; i<=3; i+=1))
do
	# time python3 auto_grade.py -v 3 -i discussion_final_results_2024-02-24_10-$i\_final_results -c all -t sampling -s 3 -d aut
	# echo auto_grade.py -v 3 -i discussion_2024-02-22_2_6_q$i\_final_results -c all -t sampling -s 3 -d aut
	python3 auto_grade.py -v 3 -i discussion_final_results_02-24_10-$i -c all -t sampling -s 3 -d aut
done