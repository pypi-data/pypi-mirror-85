TOPSIS-Anshul-101803408 is a great resource to generate TOPSIS score as well as Ranks for various model parameters, to chose the best model for the production.


### User Manual

Open your jupyter notebook and run these commands.

variable = TOPSIS()
variable.read_file("input_file_name", "output_file_name")
variable.read_weight_target("weight", "target")
variable.generate_score()
variable.generate_rank()
variable.write_file()

