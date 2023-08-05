from PerceptionToolkit.PluginInterfaces import IEventdetectionPlugin
from PerceptionToolkit.DataModel import DataModel
from PerceptionToolkit.Version import Version
from PerceptionToolkit.EyeMovementTypes import EyeMovementTypes
from typing import Sequence, List, Tuple, Any, Dict
import numpy as np
from typing import Dict, Sequence, Any
from scipy.spatial import distance
import sys



class EventdetectionIMST(IEventdetectionPlugin):
    """
    Detects fixations and saccades in the data set by using the Minimal Spanning Tree Method.

    The general setup refers to the paper "Qualitative and Quantitative Scoring and Evaluation of the Eye Movement
    Classification Algorithms" (Komogortsev et al. 2009), where the description of IMST is given in section 2.4. The
    pseudo code the this implementation is based on can be found in the appendix of that publication. Because that
    source makes use of an windows size of 200 ms, this value is used in this approach as well.

    In different papers, a change in angle of 0,5-2 degrees serves as a threshold value (see for example Stuart et al.
    2019: "Eye-tracker algorithms to detect saccades during static and dynamic tasks: a structured review").

    The implementation of the Minimal Spanning Tree of Divyanshu Mehta (see https://www.geeksforgeeks.org/prims-minimum
    -spanning-tree-mst-greedy-algo-5/ ) serves as a reference for the implementation used here.

    Attributes:
        window_size: size of the window for which the MST is constructed.
        dis_threshold: the standard value for distance in MST to evaluate whether a point is fixation or saccade.
    """

    def __init__(self):
        super(EventdetectionIMST, self).__init__()
        self.window_size = 200 # ms
        self.dis_threshold = 20

    def apply_parameters(self, parameters: Dict[str, Any]) -> None:
        self.window_size = parameters.get("window_size", self.window_size)
        self.dis_threshold = parameters.get("dis_threshold", self.dis_threshold)

    @staticmethod
    def version() -> Version:
        return Version(0, 1, 0)

    def computeDistGraph(self, arr, window_size_in_rows, data: DataModel) -> List:
        # A matrix including the distances between the points is needed as an argument for the Minimum Spanning Tree
        # Algorithm - this matrix is computed here.
        n = window_size_in_rows
        m = window_size_in_rows
        dist_graph = [[0 for j in range(m)] for i in range(n)]
        for i in range(window_size_in_rows):
            for j in range(window_size_in_rows):
                dist_graph[i][j] = distance.euclidean(arr[i], arr[j])
        return dist_graph

    class Graph():
        """
            This class is based on the MST Algorithm written by Divyanshu Mehta in https://www.geeksforgeeks.org/prims-
            minimum-spanning-tree-mst-greedy-algo-5/)
        """
        def __init__(self, vertices):
            self.V = vertices
            self.graph = [[0 for column in range(vertices)]
                          for row in range(vertices)]
            # A utility function to print the constructed MST stored in parent[]

        # minimum distance value, from the set of vertices
        # not yet included in shortest path tree
        def minKey(self, key, mstSet):
            # Initilaize min value
            min = sys.maxsize
            for v in range(self.V):
                if key[v] < min and mstSet[v] == False:
                    min = key[v]
                    min_index = v
            return min_index
            # Function to construct and print MST for a graph

        # represented using adjacency matrix representation
        def primMST(self, window_size_in_rows) -> List:
            # Key values used to pick minimum weight edge in cut
            key = [sys.maxsize] * self.V
            parent = [None] * self.V  # Array to store constructed MST
            # Make key 0 so that this vertex is picked as first vertex
            key[0] = 0
            mstSet = [False] * self.V
            parent[0] = -1  # First node is always the root of
            for cout in range(self.V):
                # Pick the minimum distance vertex from
                # the set of vertices not yet processed.
                # u is always equal to src in first iteration
                u = self.minKey(key, mstSet)
                # Put the minimum distance vertex in
                # the shortest path tree
                mstSet[u] = True
                # Update dist value of the adjacent vertices
                # of the picked vertex only if the current
                # distance is greater than new distance and
                # the vertex in not in the shortest path tree
                for v in range(self.V):
                    # graph[u][v] is non zero only for adjacent vertices of m
                    # mstSet[v] is false for vertices not yet included in MST
                    # Update the key only if graph[u][v] is smaller than key[v]
                    if self.graph[u][v] > 0 and mstSet[v] == False and key[v] > self.graph[u][v]:
                        key[v] = self.graph[u][v]
                        parent[v] = u
            n = window_size_in_rows
            m = 3
            MST = [[0 for j in range(m)] for i in range(n-1)]
            for i in range(1,n):
                MST[i-1][0]=parent[i]
                MST[i-1][1]=i
                MST[i-1][2]=self.graph[i][parent[i]]
            return MST

    def write_event(self, EventList, data: DataModel) -> None:
        """The detected fixations and saccades events are added to data.events"""
        found_events = []
        fix_counter = 0
        sac_counter = 0
        for i in range(len(EventList)):
            if fix_counter == 0 and sac_counter == 0: # only for first entry
                if EventList[i] == EyeMovementTypes.FIXATION:
                    fix_counter = 1
                if EventList[i] == EyeMovementTypes.SACCADE:
                    sac_counter = 1
                continue
            if EventList[i] == EyeMovementTypes.FIXATION and sac_counter == 0: # fixation continues
                fix_counter += 1
                continue
            if EventList[i] == EyeMovementTypes.SACCADE and fix_counter != 0: # saccade starts
                found_events.append([EyeMovementTypes.FIXATION, i-fix_counter, i-1])
                fix_counter = 0
                sac_counter = 1
                continue
            if EventList[i] == EyeMovementTypes.SACCADE and fix_counter == 0: # saccade continues
                sac_counter += 1
                continue
            if EventList[i] == EyeMovementTypes.FIXATION and sac_counter != 0: # fixation starts
                found_events.append([EyeMovementTypes.SACCADE, i-sac_counter, i-1])
                sac_counter = 0
                fix_counter = 1
                continue
            else:
                if fix_counter != 0:
                    found_events.append([EyeMovementTypes.FIXATION, i-fix_counter, i-1])
                    fix_counter = 0
                if sac_counter != 0:
                    found_events.append([EyeMovementTypes.SACCADE, i-sac_counter, i-1])
                    sac_counter = 0
        #print(found_events)
        data.remove_all_events_of_type([EyeMovementTypes.FIXATION, EyeMovementTypes.SACCADE])
        if data.events.size > 0:
            data.events = np.append(data.events, np.array(found_events), axis=0)
        else:
            data.events = np.array(found_events)

        print("Found %i Fixations." % (data.events_of_type(EyeMovementTypes.FIXATION).shape[0]))
        print("Found %i Saccades." % (data.events_of_type(EyeMovementTypes.SACCADE).shape[0]))


    def detect(self, data: DataModel) -> None:
        """
        For every window of the given window size, a minimum spanning tree is constructed. The k-loop iterates over the
        number of windows. For the last data, for which a whole window is to big, no minimum spanning tree is constructed
        and these data are not classified yet.
        """
        frames_per_ms = 1/data.ms_per_frame()
        window_size_in_rows = int(self.window_size * frames_per_ms)
        EventList = [0] * len(data.raw)
        number_of_windows = int(len(data.raw)/window_size_in_rows)
        for k in range(number_of_windows):
            arr = []
            valid = True
            for i in range(window_size_in_rows):
                # if there is invalid data within the window, there is no tree constructed
                if not data.valid()[i+k*window_size_in_rows]:
                    valid = False
                arr.append([data.x()[i+k*window_size_in_rows], data.y()[i+k*2]])
            if not valid:
                continue
            g = self.Graph(window_size_in_rows)
            g.graph = self.computeDistGraph(arr, window_size_in_rows, data)
            MST = self.Graph.primMST(g, window_size_in_rows)

            # According to the pseudo-code, we decide whether it is a saccade or a fixation based on the comparison
            # with the distance threshold
            for i in range(len(MST)):
                if MST[i][2] <= self.dis_threshold:
                    EventList[MST[i][0]+k*window_size_in_rows] = EyeMovementTypes.FIXATION
                    EventList[MST[i][1]+k*window_size_in_rows] = EyeMovementTypes.FIXATION
                if MST[i][2] > self.dis_threshold:
                    EventList[MST[i][0]+k*window_size_in_rows] = EyeMovementTypes.SACCADE
                    EventList[MST[i][1]+k*window_size_in_rows] = EyeMovementTypes.SACCADE
        # Write the found events into the data.events array

        self.write_event(EventList, data)
        #print(data.events)
        #np.savetxt("imst60.txt", data.events)
