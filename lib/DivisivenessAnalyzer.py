class DivisivenessAnalyzer:
    def __init__(self, issue, years):
        self.dataset = self.load_dataset(issue)
        self.projections = {year: self.generate_projection(year) for year in years}
        self.spectral_partitions =

    #######################################
              #  Data loading  #
    #######################################

    def load_dataset(self, issue):
        pass

    def generate_projection(self, year):
        pass

    #######################################
               #   Analysis   #
    #######################################

    """
    Up to us how we want to store this
    """
    def generate_spectral_partition(self, projection):
        pass


    #######################################
             #   Visualization   #
    #######################################

    """
    Creates a visualization
    """
    def create_visualization(self):
        pass

    def visualize(self, spectral_partition):
        pass
