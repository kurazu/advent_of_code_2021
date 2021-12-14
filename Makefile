day_01_task_1_sample:
	poetry run python -m advent.day_01.task_1 data/day_01/sample.txt

day_01_task_1_input:
	poetry run python -m advent.day_01.task_1 data/day_01/input.txt.gz

day_01_task_2_sample:
	poetry run python -m advent.day_01.task_2 data/day_01/sample.txt

day_01_task_2_input:
	poetry run python -m advent.day_01.task_2 data/day_01/input.txt.gz


day_02_task_1_sample:
	poetry run python -m advent.day_02.task_1 data/day_02/sample.txt

day_02_task_1_input:
	poetry run python -m advent.day_02.task_1 data/day_02/input.txt.gz

day_02_task_2_sample:
	poetry run python -m advent.day_02.task_2 data/day_02/sample.txt

day_02_task_2_input:
	poetry run python -m advent.day_02.task_2 data/day_02/input.txt.gz


day_03_task_1_sample:
	poetry run python -m advent.day_03.task_1 data/day_03/sample.txt

day_03_task_1_input:
	poetry run python -m advent.day_03.task_1 data/day_03/input.txt.gz

day_03_task_2_sample:
	poetry run python -m advent.day_03.task_2 data/day_03/sample.txt

day_03_task_2_input:
	poetry run python -m advent.day_03.task_2 data/day_03/input.txt.gz


day_04_task_1_sample:
	poetry run python -m advent.day_04.task_1 data/day_04/sample.txt

day_04_task_1_input:
	poetry run python -m advent.day_04.task_1 data/day_04/input.txt.gz

day_04_task_2_sample:
	poetry run python -m advent.day_04.task_2 data/day_04/sample.txt

day_04_task_2_input:
	poetry run python -m advent.day_04.task_2 data/day_04/input.txt.gz


day_05_task_1_sample:
	poetry run python -m advent.day_05.task_1 data/day_05/sample.txt

day_05_task_1_input:
	poetry run python -m advent.day_05.task_1 data/day_05/input.txt.gz

day_05_task_2_sample:
	poetry run python -m advent.day_05.task_2 data/day_05/sample.txt

day_05_task_2_input:
	poetry run python -m advent.day_05.task_2 data/day_05/input.txt.gz


day_06_task_1_sample:
	poetry run python -m advent.day_06.task_1 data/day_06/sample.txt

day_06_task_1_input:
	poetry run python -m advent.day_06.task_1 data/day_06/input.txt.gz

day_06_task_2_sample:
	poetry run python -m advent.day_06.task_2 data/day_06/sample.txt

day_06_task_2_input:
	poetry run python -m advent.day_06.task_2 data/day_06/input.txt.gz


day_07_task_1_sample:
	poetry run python -m advent.day_07.task_1 data/day_07/sample.txt

day_07_task_1_input:
	poetry run python -m advent.day_07.task_1 data/day_07/input.txt.gz

day_07_task_2_sample:
	poetry run python -m advent.day_07.task_2 data/day_07/sample.txt

day_07_task_2_input:
	poetry run python -m advent.day_07.task_2 data/day_07/input.txt.gz


day_08_task_1_sample:
	poetry run python -m advent.day_08.task_1 data/day_08/sample.txt

day_08_task_1_input:
	poetry run python -m advent.day_08.task_1 data/day_08/input.txt.gz

day_08_task_2_sample:
	poetry run python -m advent.day_08.task_2 data/day_08/sample.txt

day_08_task_2_input:
	poetry run python -m advent.day_08.task_2 data/day_08/input.txt.gz


day_09_task_1_sample:
	poetry run python -m advent.day_09.task_1 data/day_09/sample.txt

day_09_task_1_input:
	poetry run python -m advent.day_09.task_1 data/day_09/input.txt.gz

day_09_task_2_sample:
	poetry run python -m advent.day_09.task_2 data/day_09/sample.txt

day_09_task_2_input:
	poetry run python -m advent.day_09.task_2 data/day_09/input.txt.gz


day_10_task_1_sample:
	poetry run python -m advent.day_10.task_1 data/day_10/sample.txt

day_10_task_1_input:
	poetry run python -m advent.day_10.task_1 data/day_10/input.txt.gz

day_10_task_2_sample:
	poetry run python -m advent.day_10.task_2 data/day_10/sample.txt

day_10_task_2_input:
	poetry run python -m advent.day_10.task_2 data/day_10/input.txt.gz


day_11_task_1_sample:
	poetry run python -m advent.day_11.task_1 data/day_11/sample.txt

day_11_task_1_input:
	poetry run python -m advent.day_11.task_1 data/day_11/input.txt.gz

day_11_task_2_sample:
	poetry run python -m advent.day_11.task_2 data/day_11/sample.txt

day_11_task_2_input:
	poetry run python -m advent.day_11.task_2 data/day_11/input.txt.gz


visualize_day_12_samples:
	poetry run python -m advent.day_12.visualize \
		--input=data/day_12/sample.txt \
		--output=data/day_12/sample.png
	poetry run python -m advent.day_12.visualize \
		--input=data/day_12/larger-sample.txt \
		--output=data/day_12/larger-sample.png
	poetry run python -m advent.day_12.visualize \
		--input=data/day_12/largest-sample.txt \
		--output=data/day_12/largest-sample.png
	poetry run python -m advent.day_12.visualize \
		--input=data/day_12/input.txt \
		--output=data/day_12/input.png

day_12_task_1_sample:
	poetry run python -m advent.day_12.task_1 data/day_12/sample.txt

day_12_task_1_larger_sample:
	poetry run python -m advent.day_12.task_1 data/day_12/larger-sample.txt

day_12_task_1_largest_sample:
	poetry run python -m advent.day_12.task_1 data/day_12/largest-sample.txt

day_12_task_1_input:
	poetry run python -m advent.day_12.task_1 data/day_12/input.txt

day_12_task_2_sample:
	poetry run python -m advent.day_12.task_2 data/day_12/sample.txt

day_12_task_2_larger_sample:
	poetry run python -m advent.day_12.task_2 data/day_12/larger-sample.txt

day_12_task_2_largest_sample:
	poetry run python -m advent.day_12.task_2 data/day_12/largest-sample.txt

day_12_task_2_input:
	poetry run python -m advent.day_12.task_2 data/day_12/input.txt


day_13_task_1_sample:
	poetry run python -m advent.day_13.task_1 data/day_13/sample.txt

day_13_task_1_input:
	poetry run python -m advent.day_13.task_1 data/day_13/input.txt.gz

day_13_task_2_sample:
	poetry run python -m advent.day_13.task_2 data/day_13/sample.txt

day_13_task_2_input:
	poetry run python -m advent.day_13.task_2 data/day_13/input.txt.gz


day_14_task_1_sample:
	poetry run python -m advent.day_14.task_1 data/day_14/sample.txt

day_14_task_1_input:
	poetry run python -m advent.day_14.task_1 data/day_14/input.txt.gz

day_14_task_2_sample:
	poetry run python -m advent.day_14.task_2 data/day_14/sample.txt

day_14_task_2_input:
	poetry run python -m advent.day_14.task_2 data/day_14/input.txt.gz
