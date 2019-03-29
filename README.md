# Kodama generator
Do you know those little beings in Princess Mononoke? We intented to generate them in 3D thanks to a genetic algorithm in python for Blender and export them to a specific folder.
------
Just import ```src/algo.py``` into the scripts of the Blender file. Then run. It should export the number of Kodama you have decided at the top of the python file into the exports folder.

## Order of the genetic algorithm:
1. Define the characteristics of a Kodama (chromosome).
2. Translate the genes thanks to a class.
3. Create the population randomly.
4. Decode the genotype to get the phenotype, in other words the 3D representation of a Kodama.
7. Fitness evaluation, gives a good mark to the fittest Kodamas.
10. Main loop with each time: selection of parents, crossover (children) and mutation.

**By Pauline Legros & Ugo Bouveron.**
