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


day_15_task_1_sample:
	poetry run python -m advent.day_15.task_1 data/day_15/sample.txt

day_15_task_1_input:
	poetry run python -m advent.day_15.task_1 data/day_15/input.txt.gz

day_15_task_2_sample:
	poetry run python -m advent.day_15.task_2 data/day_15/sample.txt

day_15_task_2_input:
	poetry run python -m advent.day_15.task_2 data/day_15/input.txt.gz


day_16_task_1_sample_1:
	poetry run python -m advent.day_16.task_1 data/day_16/sample_1.txt

day_16_task_1_sample_2:
	poetry run python -m advent.day_16.task_1 data/day_16/sample_2.txt

day_16_task_1_sample_3:
	poetry run python -m advent.day_16.task_1 data/day_16/sample_3.txt

day_16_task_1_sample_4:
	poetry run python -m advent.day_16.task_1 data/day_16/sample_4.txt

day_16_task_1_sample_5:
	poetry run python -m advent.day_16.task_1 data/day_16/sample_5.txt

day_16_task_1_sample_6:
	poetry run python -m advent.day_16.task_1 data/day_16/sample_6.txt

day_16_task_1_sample_7:
	poetry run python -m advent.day_16.task_1 data/day_16/sample_7.txt

day_16_task_1_input:
	poetry run python -m advent.day_16.task_1 data/day_16/input.txt.gz

day_16_task_2_sample:
	poetry run python -m advent.day_16.task_2 data/day_16/sample.txt

day_16_task_2_input:
	poetry run python -m advent.day_16.task_2 data/day_16/input.txt.gz


day_17_task_1_sample:
	poetry run python -m advent.day_17.task_1 data/day_17/sample.txt

day_17_task_1_input:
	poetry run python -m advent.day_17.task_1 data/day_17/input.txt

day_17_task_2_sample:
	poetry run python -m advent.day_17.task_2 data/day_17/sample.txt

day_17_task_2_input:
	poetry run python -m advent.day_17.task_2 data/day_17/input.txt


day_18_task_1_test:
	poetry run pytest -s -vv advent/day_18/test_task_1.py

day_18_task_1_sample:
	poetry run python -m advent.day_18.task_1 data/day_18/sample.txt

day_18_task_1_input:
	poetry run python -m advent.day_18.task_1 data/day_18/input.txt

day_18_task_2_sample:
	poetry run python -m advent.day_18.task_2 data/day_18/sample.txt

day_18_task_2_input:
	poetry run python -m advent.day_18.task_2 data/day_18/input.txt


day_19_task_1_sample:
	poetry run python -m advent.day_19.task_1 data/day_19/sample.txt

day_19_task_1_input:
	poetry run python -m advent.day_19.task_1 data/day_19/input.txt.gz

day_19_task_2_sample:
	poetry run python -m advent.day_19.task_2 data/day_19/sample.txt

day_19_task_2_input:
	poetry run python -m advent.day_19.task_2 data/day_19/input.txt.gz


day_20_task_1_sample:
	poetry run python -m advent.day_20.task_1 data/day_20/sample.txt

day_20_task_1_input:
	poetry run python -m advent.day_20.task_1 data/day_20/input.txt.gz

day_20_task_2_sample:
	poetry run python -m advent.day_20.task_2 data/day_20/sample.txt

day_20_task_2_input:
	poetry run python -m advent.day_20.task_2 data/day_20/input.txt.gz


day_21_task_1_sample:
	poetry run python -m advent.day_21.task_1 data/day_21/sample.txt

day_21_task_1_input:
	poetry run python -m advent.day_21.task_1 data/day_21/input.txt

day_21_task_2_sample:
	poetry run python -m advent.day_21.task_2 data/day_21/sample.txt

day_21_task_2_input:
	poetry run python -m advent.day_21.task_2 data/day_21/input.txt


day_22_task_1_sample:
	poetry run python -m advent.day_22.task_1 data/day_22/sample.txt

day_22_task_1_input:
	poetry run python -m advent.day_22.task_1 data/day_22/input.txt.gz

day_22_task_2_sample:
	poetry run python -m advent.day_22.task_2 data/day_22/sample.txt

day_22_task_2_tiny_sample:
	poetry run python -m advent.day_22.task_2 data/day_22/tiny_sample.txt

day_22_task_2_big_sample:
	poetry run python -m advent.day_22.task_2 data/day_22/big_sample.txt

day_22_task_2_input:
	poetry run python -m advent.day_22.task_2 data/day_22/input.txt.gz

day_22_task_2_test:
	poetry run pytest -s -vv -x advent/day_22/test_task_2.py


day_23_task_1_sample:
	poetry run python -m advent.day_23.task_1 data/day_23/sample.txt

day_23_test:
	poetry run pytest -s -vv advent/day_23/test_*.py

day_23_task_1_input:
	poetry run python -m advent.day_23.task_1 data/day_23/input.txt

day_23_task_2_sample:
	poetry run python -m advent.day_23.task_2 data/day_23/sample.txt

day_23_task_2_input:
	poetry run python -m advent.day_23.task_2 data/day_23/input.txt


day_24_task_1_sample:
	poetry run python -m advent.day_24.task_1 data/day_24/sample.txt

day_24_task_1_input:
	poetry run python -m advent.day_24.task_1 data/day_24/input.txt.gz

day_24_task_2_sample:
	poetry run python -m advent.day_24.task_2 data/day_24/sample.txt

day_24_task_2_input:
	poetry run python -m advent.day_24.task_2 data/day_24/input.txt.gz
