# for i in {2..8}; do
#     echo python_script.py "discussion_final_results_02-21_02:02:39_2_$i"
# done

for ((i=2; i<=10; i+=2))
do
	time python3 auto_grade.py -v 3 -i discussion_final_results_02-21_2_$i -c all -t sampling -s 3 -d aut
done