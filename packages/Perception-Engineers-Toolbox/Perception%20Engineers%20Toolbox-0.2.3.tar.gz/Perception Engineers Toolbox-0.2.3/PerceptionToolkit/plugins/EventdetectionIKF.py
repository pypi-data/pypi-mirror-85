from PerceptionToolkit.PluginInterfaces import IEventdetectionPlugin
import numpy as np
from PerceptionToolkit.DataModel import DataModel
from PerceptionToolkit.EyeMovementTypes import EyeMovementTypes
from typing import Sequence, Dict, Any
from PerceptionToolkit.EventdetectionHelpers import VelocityCalculatorPixels
from PerceptionToolkit.Version import Version
from pomegranate import HiddenMarkovModel, NormalDistribution, State, GeneralMixtureModel
import math


class EventdetectionIKF(IEventdetectionPlugin):
    """
    """

    def __init__(self):
        super(EventdetectionIKF, self).__init__()

        self.velocity_calculator_window = 20  # ms

        self.chi2threshold = 10
        self.kalmanFilterParameter1 = 1
        self.kalmanFilterParameter2 = 1

    def apply_parameters(self, parameters: Dict[str, Any]) -> None:

        self.velocity_calculator_window = parameters.get("velocity_calculator_window", self.velocity_calculator_window)

        self.chi2threshold = parameters.get("chi2threshold", self.chi2threshold)
        self.kalmanFilterParameter1 = parameters.get("kalmanFilterParameter1", self.kalmanFilterParameter1)
        self.kalmanFilterParameter1 = parameters.get("kalmanFilterParameter1", self.kalmanFilterParameter1)

    @staticmethod
    def version() -> Version:
        return Version(0, 1, 0)

    """Following Kalman Filter algorithm based on: 
        https://stackoverflow.com/questions/3337301/numpy-matrix-to-array"""

    def kalman_xy(self, x, P, measurement, R,
                  motion=np.array([[0., 0., 0., 0.]]).T,
                  Q = np.eye(4)):
        """
        Parameters:
        x: initial state 4-tuple of location and velocity: (x, y, vel_x, vel_y)
        P: initial uncertainty covariance matrix
        measurement: observed position
        R: measurement noise
        motion: external motion added to state vector x
        Q: motion noise (same shape as P)
        """
        return self.kalman(x, P, measurement, R, motion, Q,
                      F = np.array([[1., 0., 1., 0.], [0., 1., 0., 1.], [0., 0., 1., 0.], [0., 0., 0., 1.]]),
                      H = np.array([[1., 0., 0., 0.], [0., 1., 0., 0.]]))

    def kalman(self, x, P, measurement, R, motion, Q, F, H):
        '''
        Parameters:
        x: initial state
        P: initial uncertainty convariance matrix
        measurement: observed position (same shape as H*x)
        R: measurement noise (same shape as H)
        motion: external motion added to state vector x
        Q: motion noise (same shape as P)
        F: next state function: x_prime = F*x
        H: measurement function: position = H*x

        Return: the updated and predicted new values for (x, P)

        See also http://en.wikipedia.org/wiki/Kalman_filter

        This version of kalman can be applied to many different situations by
        appropriately defining F and H
        '''
        # UPDATE x, P based on measurement m
        # distance between measured and current position-belief
        y = np.array(measurement).T - np.matmul(H, x)
        S = np.matmul(np.matmul(H,P),H.T) + R # residual covariance
        K = np.matmul(np.matmul(P, H.T),np.linalg.inv(S)) # Kalman gain
        x = x + np.matmul(K,y)
        I = np.eye(F.shape[0]) # identity matrix
        P = np.matmul(I - np.matmul(K,H), P)

        # PREDICT x, P based on motion
        x = np.matmul(F,x)+ motion
        P = np.matmul(np.matmul(F,P),F.T)+Q
        return x, P

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
        # Calculate actual velocities

        real_x_vel = []
        real_y_vel = []

        for i in range(len(data.x())-1):
            real_x_vel.append((math.sqrt(pow(data.x()[i + 1] - data.x()[i], 2))) / (data.time()[i + 1]-data.time()[i]))
            real_y_vel.append((math.sqrt(pow(data.y()[i + 1] - data.y()[i], 2))) / (data.time()[i + 1] - data.time()[i]))

        # Calculate predicted velocities with Kalman Filter
        x = np.array([[data.x()[0], data.y()[0], real_x_vel[0], real_y_vel[0]]]).T
        P = 1000 * np.eye(4)  # initial uncertainty

        observed_x = data.x()
        observed_y = data.y()
        result_pos = []
        result_vel = []
        R = 0.01 ** 2
        for meas in zip(observed_x, observed_y):
            x, P = self.kalman_xy(x, P, meas, R)
            result_pos.append((x[:2]).tolist())
            result_vel.append((x[2:4]).tolist())
        kalman_x_pos, kalman_y_pos = zip(*result_pos)
        kalman_x_vel, kalman_y_vel = zip(*result_vel)


        predicted_x_pos = []
        predicted_y_pos = []
        for i in range(len(kalman_x_pos)):
            predicted_x_pos.append(kalman_x_pos[i][0])
            predicted_y_pos.append(kalman_x_pos[i][1])

        predicted_x_vel = []
        predicted_y_vel = []
        for i in range(len(kalman_x_vel)):
            predicted_x_vel.append(abs(kalman_x_vel[i][0]))
            predicted_y_vel.append(abs(kalman_x_vel[i][1]))

        # Calculate Chi square for velocity
        std_vel_x = np.std(real_x_vel)
        std_vel_y = np.std(real_y_vel)

        chi_square = []
        for i in range(len(real_x_vel)):
            chi_square_x = (predicted_x_vel[i] - real_x_vel[i])**2 / std_vel_x**2
            chi_square_y = (predicted_y_vel[i] - real_y_vel[i])**2 / std_vel_y**2
            chi_square.append(chi_square_x + chi_square_y)

        # Compare each chi square to chi square threshold and determine its event type
        EventList = [0] * len(chi_square)
        for i in range(len(chi_square)):
            if chi_square[i] <= self.chi2threshold:
                EventList[i] = EyeMovementTypes.FIXATION
            if chi_square[i] > self.chi2threshold:
                EventList[i] = EyeMovementTypes.SACCADE

        self.write_event(EventList, data)