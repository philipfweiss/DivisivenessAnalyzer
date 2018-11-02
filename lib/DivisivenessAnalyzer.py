import SpectralPartition
# import DivisivenessVisualizer

class DivisivenessAnalyzer:
    def __init__(self, issue, years):
        self.dataset = self.load_dataset(issue)
        self.projections = {year: self.generate_projection(year) for year in years}
        self.spectral_partitions = self.generate_spectral_partitions()

    #######################################
              #  Data loading  #
    #######################################

    def load_dataset(self, issue):
        pass

    """
    Generates the issue projection for a given year. Should save the file
    and try to repopulate from cache.
    """
    def generate_projection(self, year):
        pass

    """
    Given a congressional graph projection, generates the associated spectral partition.
    Perhaps should save a picked version of obj?
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
