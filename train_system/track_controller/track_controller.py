
#Track Controller
from ..common import TrackBlock

class TrackController:
    def __init__(self):
        """
        Initialize the Track Controller.
        """

        self.track_occupancies = {}
        self.train_suggested_speeds = {}
        self.train_authorities = {}
    
    def compute_suggested_speed(self):
        """
        Compute the suggested speed for each train based on track occupancy.

        Returns:
            float: Suggested speed for the train.
        """
    
    def compute_authority(self, train_id: int):
        """
        Compute the authority for each train.
        
        Args:
            train_id (int): Identifier for the train.
        
        Returns:
            int: Authority for the train.
        """
    