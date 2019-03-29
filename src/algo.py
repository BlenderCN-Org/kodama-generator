import bpy, bmesh, random, os, operator

#---VARIABLES---
PRECISION = 3 # more precision equals more meshes
MAX_GEN = 30 # the more generation the more ideal will be the Kodamas
KODAMA_NB = 10 # total number of Kodama which will be exported
# Don't touch
GENERATION = 0
POPULATION = []

#Material
white = bpy.data.materials.new(name="Mat.White")
white.diffuse_color = (1, 1, 1)

#1 Kodama = chromosome
class Kodama:
    #2 Genes
    def __init__(self, height, eyeLSize, eyeRSize, eyeLShape, eyeRShape, between, mouth, head, weight):
        self.height = height
        self.eyeLSize = eyeLSize
        self.eyeRSize = eyeRSize
        self.eyeLShape = eyeLShape
        self.eyeRShape = eyeRShape
        self.between = between
        self.mouth = mouth
        self.head = head 
        self.weight = weight
    
    def __repr__(self):
        return "Un kodama"
    
    #Can be improved
    def mutate(self, mutationRate):
        if (random.random() < mutationRate):
            hei = self.height
            self.height = self.weight + 0.2
            self.weight = hei - 0.2
        if (random.random() < mutationRate):
            size = self.eyeLSize
            self.eyeLSize = self.eyeRSize
            self.eyeRSize = size
        if (random.random() < mutationRate):
            shape = self.eyeLShape
            self.eyeLShape = self.eyeRShape
            self.eyeRShape = shape
        return self


#7 Fitness
class Fitness:
    def __init__(self, kod):
        self.kodama = kod
        self.fitness = 0.0
        self.score = 0
        self.best = Kodama(1, 0.15, 0, 0.15, 0, 0.4, 0, 0.1, 0.8) #The fittest individual
    
    #Compares each characteristic towards the best Kodama    
    def chromoFit(self):
        if self.score == 0:
            self.score += abs(self.best.height - self.kodama.height)
            self.score += abs(self.best.eyeLSize - self.kodama.eyeLSize)
            self.score += abs(self.best.eyeLShape - self.kodama.eyeLShape)
            self.score += abs(self.best.eyeRSize - self.kodama.eyeRSize)
            self.score += abs(self.best.eyeRShape- self.kodama.eyeRShape)
            self.score += abs(self.best.between - self.kodama.between)
            self.score += abs(self.best.mouth - self.kodama.mouth)
            self.score += abs(self.best.head - self.kodama.head)
            self.score += abs(self.best.weight - self.kodama.weight)
        return self.score
    
    # The bigger is the fitness, the better is the Kodama    
    def kodamaFitness(self):
        if self.fitness == 0:
            self.fitness = 1 / float(self.chromoFit())
        return self.fitness
    
    def __repr__(self):
        return "Un fitness"

#---FUNCTIONS---

#Automatic cleaning of the scene each time we run the script
def clear():
    for obj in bpy.data.objects:
        obj.select = True
    bpy.ops.object.delete()

#3 Generate the population randomly
def generate(NB):
    for i in range(0, NB):
        POPULATION.append(Kodama(random.uniform(0.8, 1.2), random.uniform(0, 0.3), random.uniform(-0.15, 0.15), random.uniform(0, 0.3), random.uniform(-0.15, 0.15), random.uniform(0.2, 0.5), random.uniform(-1.0, 1.0), random.uniform(-0.3, 0.3), random.uniform(0.6, 1)))
    return POPULATION

#4 Draws the population in Blender by decoding the genotype
def phenotype(index):
    clear()
    
    #EyeL
    bpy.ops.mesh.primitive_ico_sphere_add(size=POPULATION[index].eyeLSize, subdivisions=PRECISION, calc_uvs=False, view_align=False, enter_editmode=False, location=(0.7 + POPULATION[index].weight - 0.8, -POPULATION[index].between, 3.2), layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))
    bpy.ops.transform.resize(value=(1.5, 1, 1), constraint_axis=(True, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
    bpy.context.object.name = "EyeL"
    bpy.ops.object.modifier_add(type='SIMPLE_DEFORM')
    bpy.context.object.modifiers["SimpleDeform"].deform_method = 'STRETCH'
    bpy.context.object.modifiers["SimpleDeform"].factor = POPULATION[index].eyeLShape
    
    #EyeR
    bpy.ops.mesh.primitive_ico_sphere_add(size=POPULATION[index].eyeRSize, subdivisions=PRECISION, calc_uvs=False, view_align=False, enter_editmode=False, location=(0.7 + POPULATION[index].weight - 0.8, POPULATION[index].between, 3.2), layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))
    bpy.ops.transform.resize(value=(1.5, 1, 1), constraint_axis=(True, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
    bpy.context.object.name = "EyeR"
    bpy.ops.object.modifier_add(type='SIMPLE_DEFORM')
    bpy.context.object.modifiers["SimpleDeform"].deform_method = 'STRETCH'
    bpy.context.object.modifiers["SimpleDeform"].factor = POPULATION[index].eyeRShape
    
    #Mouth
    bpy.ops.mesh.primitive_ico_sphere_add(size=0.3, subdivisions=PRECISION, calc_uvs=False, view_align=False, enter_editmode=False, location=(0.7 + POPULATION[index].weight*0.1, 0, 2.7), layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))
    bpy.ops.transform.resize(value=(0.5, 1, 0.5), constraint_axis=(False, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
    bpy.context.object.name = "Mouth"
    
    bpy.ops.object.modifier_add(type='SIMPLE_DEFORM')
    bpy.context.object.modifiers["SimpleDeform"].deform_method = 'STRETCH'
    bpy.context.object.modifiers["SimpleDeform"].factor = POPULATION[index].mouth
    bpy.ops.object.modifier_apply(apply_as='DATA', modifier="SimpleDeform")
    bpy.ops.object.modifier_add(type='SIMPLE_DEFORM')
    bpy.context.object.modifiers["SimpleDeform"].deform_method = 'TAPER'
    bpy.context.object.modifiers["SimpleDeform"].factor = POPULATION[index].mouth * POPULATION[index].head
    
    #HEAD
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=PRECISION+1, view_align=False, enter_editmode=False, location=(0, 0, 2+POPULATION[index].height), layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))
    bpy.ops.transform.resize(value=(POPULATION[index].weight, 1, POPULATION[index].height), constraint_axis=(False, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
    bpy.context.object.name = "Head"
    bpy.context.object.active_material = white
    
    bpy.ops.object.modifier_add(type='SIMPLE_DEFORM')
    bpy.context.object.modifiers["SimpleDeform"].deform_method = 'STRETCH'
    bpy.context.object.modifiers["SimpleDeform"].factor = POPULATION[index].head
    
    bpy.ops.object.modifier_add(type='BOOLEAN')
    bpy.context.object.modifiers["Boolean"].object = bpy.data.objects["EyeL"]
    bpy.context.object.modifiers["Boolean"].operation = 'DIFFERENCE'
    bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Boolean")
    
    bpy.ops.object.modifier_add(type='BOOLEAN')
    bpy.context.object.modifiers["Boolean"].object = bpy.data.objects["EyeR"]
    bpy.context.object.modifiers["Boolean"].operation = 'DIFFERENCE'
    bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Boolean")
    
    bpy.ops.object.modifier_add(type='BOOLEAN')
    bpy.context.object.modifiers["Boolean"].object = bpy.data.objects["Mouth"]
    bpy.context.object.modifiers["Boolean"].operation = 'DIFFERENCE'
    bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Boolean")
    bpy.ops.object.shade_smooth()
    
    #Delete
    bpy.data.objects["Head"].select = False
    bpy.data.objects["EyeL"].select = True
    bpy.data.objects["EyeR"].select = True
    bpy.data.objects["Mouth"].select = True
    bpy.ops.object.delete(use_global = False)
    
    #Body
    file_loc = bpy.data.filepath
    imported_object = bpy.ops.import_scene.obj(filepath=file_loc.replace("algo.blend", "src/body.obj"))
    body_object = bpy.context.selected_objects[0]
    body_object.name = "Body"
    bpy.ops.object.origin_set(type='GEOMETRY_ORIGIN')
    body_object.location = (0,0,1)
    body_object.active_material = white
    body_object.scale = (POPULATION[index].weight*2.6, 2.5,POPULATION[index].height*2.5)
    
#5 Apply mutate to the whole popul array
def mutation(popul, mutationRate):
    mutatedPop = []
    for i in range(0, len(popul)):
        mutatedInd = popul[i].mutate(mutationRate)
        mutatedPop.append(mutatedInd)
    return mutatedPop
    
#6 Ordered crossover, a random part of the genes are combined on the selected Kodamas
def crossover(matingPool, eliteSize):
    children = []
    
    length = len(matingPool) - eliteSize
    pool = random.sample(matingPool, len(matingPool))
    
    # Best Kodamas parents automatically become children
    for i in range(0, eliteSize):
        children.append(matingPool[i])
    
    # For the others we take pairs of parent
    for i in range(0, length):
        child = Kodama(pool[len(matingPool)-i-1].height, pool[len(matingPool)-i-1].eyeLSize, pool[len(matingPool)-i-1].eyeRSize, pool[len(matingPool)-i-1].eyeLShape, pool[len(matingPool)-i-1].eyeRShape, pool[len(matingPool)-i-1].between, pool[len(matingPool)-i-1].mouth, pool[len(matingPool)-i-1].head, pool[len(matingPool)-i-1].weight)
        
        #There are 8 characteristics starting from 0
        geneA = int(random.random()*8)
        geneB = int(random.random()*8)
        
        startGene = min(geneA, geneB)
        endGene = max(geneA, geneB)
        
        if (startGene <= 0 <= endGene):
            child.height = pool[i].height
        if (startGene <= 1 <= endGene):
            child.eyeLSize = pool[i].eyeLSize
        if (startGene <= 2 <= endGene):
            child.eyeRSize = pool[i].eyeRSize
        if (startGene <= 3 <= endGene):
            child.eyeLShape = pool[i].eyeLShape
        if (startGene <= 4 <= endGene):
            child.eyeRShape = pool[i].eyeRShape
        if (startGene <= 5 <= endGene):
            child.between = pool[i].between
        if (startGene <= 6 <= endGene):
            child.mouth = pool[i].mouth
        if (startGene <= 7 <= endGene):
            child.head = pool[i].head
        if (startGene <= 8 <= endGene):
            child.weight = pool[i].weight
        
        children.append(child)
    return children
    
#8 Fitness proportionate selection with elitism
def parentSelection(popRanked, eliteSize):
    selectionResults = []
    fitnessSum = 0
    fitnessIndiv = []
    for i in range(0, len(popRanked)):
        fit = popRanked[i][0]
        fitnessSum += fit
        fitnessIndiv.append(fit)
    
    # Get a % for each individual
    for indiv in fitnessIndiv:
        indiv = 100 * indiv / fitnessSum
    
    #Elistim
    for i in range(0, eliteSize):
        selectionResults.append(popRanked[i][0])
        
    #Random number to compare 
    for j in range(0, len(popRanked) - eliteSize):
        pick = 100*random.random()
        for i in range(0, len(popRanked)):
            if pick <= fitnessIndiv[i]:
                selectionResults.append(popRanked[i][0])
                break
    
    #Extract the selected Kodamas
    matingpool = []
    for i in range(0, len(selectionResults)):
        index = selectionResults[i]
        matingpool.append(POPULATION[index])
    return matingpool

#9 Ranking of the fittest Kodamas
def evaluate(gen):
    fitnessResults = {}
    for i in range(0, len(POPULATION)):
        fitnessResults[i] = Fitness(POPULATION[i]).kodamaFitness()
    return sorted(fitnessResults.items(), key = operator.itemgetter(1), reverse = True) 
    

#10 Main loop
def nextGeneration(currentGen, eliteSize, mutationRate):
    #9
    popRanked = evaluate(POPULATION)
    #8
    matingPool = parentSelection(popRanked, eliteSize)
    #6
    children = crossover(matingPool, eliteSize)
    #5
    nextGen = mutation(children, mutationRate)
    return nextGen
        
# The genetic algorithm which initiates and does the loop     
def main(popSize, eliteSize, mutationRate):
    global GENERATION
    POPULATION = generate(popSize)    
    while (GENERATION < MAX_GEN):
        print(GENERATION)
        POPULATION = nextGeneration(POPULATION, eliteSize, mutationRate)
        phenotype(0)
        GENERATION += 1
        
# Export the population as OBJ files in an exports folder       
def export():
    file_loc = bpy.data.filepath
    directory = os.path.dirname(file_loc) + "\exports"
    kod = "kodama_"
    for i in range(0, len(POPULATION)):
        name = kod + str(i) + ".obj"
        target_file = os.path.join(directory, name)
        phenotype(i)
        bpy.ops.export_scene.obj(filepath=target_file, check_existing=True, axis_forward='-Z', axis_up='Y', filter_glob="*.obj;*.mtl", use_selection=False, use_animation=False, use_mesh_modifiers=True, use_edges=True, use_smooth_groups=False, use_smooth_groups_bitflags=False, use_normals=True, use_uvs=True, use_materials=True, use_triangles=False, use_nurbs=False, use_vertex_groups=False, use_blen_objects=True, group_by_object=False, group_by_material=False, keep_vertex_order=False, global_scale=1, path_mode='AUTO')

#---EXECUTION---

main(KODAMA_NB, 3, 0.01)
export()