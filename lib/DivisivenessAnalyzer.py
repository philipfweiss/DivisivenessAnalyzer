import SpectralPartition
# import DivisivenessVisualizer

class DivisivenessAnalyzer:
    def __init__(self, issue, years):
        self.issue = issue
        self.projections = {year: self.load_projection(year) for year in years}
        self.spectral_partitions = self.generate_spectral_partitions()

    #######################################
              #  Data loading  #
    #######################################
    """
    Loads the issue projections for a given year.
    Found in dataset/<issue>/<year>.graph
    """
    def load_projection(self, year):
        pass

    """
    Given a congressional graph projection, generates the associated spectral partition.
    Perhaps should save a pickled version of obj?
    """
    def generate_spectral_partitions(self):

        # First, look to see if we have the partition cached. If not, then
        # we generate the actual partition.

        return {
            year: SpectralPartition(projection) for year, projection in self.projections.items()
        }

    #######################################
             #   Visualization   #
    #######################################

    """
    Creates a visualization of our spectral partitions.
    Optional: Use the DivisivenessVisualizer class?
    """
    def create_visualization(self):
        pass
