from .SimpfulModelBuilder import SugenoFISBuilder
import numpy as np

class FireStrengthCalculator(object):
     def __init__(self, antecedent_parameters, variable_names, nr_clus, **kwargs):
           
    
        # Build a first-order Takagi-Sugeno model using Simpful using dummy consequent parameters
        if 'operators' not in kwargs.keys(): kwargs['operators'] = None
        simpbuilder = SugenoFISBuilder(
            self.antecedent_parameters, 
            np.tile(1, (self.nr_clus, len(self.variable_names)+1)), 
            self.variable_names, 
            extreme_values = self._antecedent_estimator._extreme_values,
            operators=kwargs["operators"], 
            save_simpful_code=False, 
            fuzzy_sets_to_drop=what_to_drop)

        self.dummymodel = simpbuilder.simpfulmodel
        
        # Calculate the firing strengths for each rule for each data point 
        firing_strengths=[]
        print(self.variable_names)
        for i in range(0,len(self.x_train)):
            for j in range (0,len(self.variable_names)):
                self.dummymodel.set_variable(self.variable_names[j], self.x_train[i,j])
            firing_strengths.append(self.dummymodel.get_firing_strenghts())
        self.firing_strengths=np.array(firing_strengths)
        