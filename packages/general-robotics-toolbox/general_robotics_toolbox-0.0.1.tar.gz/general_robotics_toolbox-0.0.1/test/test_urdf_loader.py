#!/usr/bin/env python

import unittest
import general_robotics_toolbox as rox
from general_robotics_toolbox import urdf
import numpy as np

class Test_irb6640(unittest.TestCase):

    def runTest(self):        
        robot = urdf.robot_from_xacro_file("test/irb6640_180_255_nogeom.xacro", "rpi_general_robotics_toolbox_py")
        self.assert_robot(robot)
        robot2 = urdf.robot_from_xml_file("test/irb6640_180_255_nogeom.urdf", "rpi_general_robotics_toolbox_py")
        self.assert_robot(robot2)
        robot3 = urdf.robot_from_xml_file("test/irb6640_180_255_nogeom_twist.urdf", "rpi_general_robotics_toolbox_py")        
        self.assert_robot(robot3)
        
    def assert_robot(self, robot):
        np.testing.assert_allclose(robot.H, np.array([[0.,0.,0.,1.,0.,1.],[0.,1.,1.,0.,1.,0.],[1.,0.,0.,0.,0.,0.]]), atol=1e-4)
        np.testing.assert_allclose(robot.P, np.array([[0.,0.32,0.,0.,1.142,0.2,0.],[0.,0.,0.,0.,0.,0.,0.],[0.78,0.,1.075,0.2,0.,0.,0.]]), atol=1e-4)
        np.testing.assert_allclose(robot.joint_type, np.array([0.,0.,0.,0.,0.,0.]), atol=1e-4)
        np.testing.assert_allclose(robot.joint_lower_limit, np.array([-2.967,-1.134,-3.142,-5.236,-2.094,-6.283]), atol=1e-4)
        np.testing.assert_allclose(robot.joint_upper_limit, np.array([2.967,1.4855,1.222,5.236,2.094,6.283]), atol=1e-4)
        np.testing.assert_allclose(robot.joint_vel_limit, np.array([1.7453,1.5707,1.5707,2.9671,2.4435,3.3161]), atol=1e-4)
        np.testing.assert_allclose(robot.R_tool, np.array([[0,0,1], [0,1,0], [-1,0,0]]), atol=1e-4)
        np.testing.assert_allclose(robot.p_tool, [0,0,0], atol=1e-4)
    
class Test_sda10f(unittest.TestCase):
    
    def runTest(self):
        with self.assertRaises(AssertionError):
            urdf.robot_from_xml_file("test/sda10f_nogeom.urdf", "rpi_general_robotics_toolbox_py")
        
        left_robot = urdf.robot_from_xml_file("test/sda10f_nogeom.urdf", "rpi_general_robotics_toolbox_py", tip_link='arm_left_link_tool0')
        self.assert_left_robot(left_robot)
        
        right_robot = urdf.robot_from_xml_file("test/sda10f_nogeom.urdf", "rpi_general_robotics_toolbox_py", root_link='torso_link_b1', tip_link='arm_right_link_tool0')
        self.assert_right_robot(right_robot)
    
    def assert_left_robot(self, robot):
        np.testing.assert_allclose(robot.H, np.array([[0.,0.,0.,0.,0.,0.,0.,0.],[0.,1.,0.,1.,0.,-1.,0.,1.],[1.,0,-1.,0.,1.,0.,1.,0.]]), atol=1e-4)
        np.testing.assert_allclose(robot.P, np.array([[0.0926,0.0999,0.,0.,0.,0.,0.,0.,0.],[0.,0.0275,0.2255,0.169,0.181,0.1936,0.155,0.168,0.],[0.8835,0.3221,0.0577,-0.0454,-0.0085,0.0155,0.008,-0.015,0.]]), atol=1e-4)
        np.testing.assert_allclose(robot.joint_type, np.array([0.,0.,0.,0.,0.,0.,0.,0.]), atol=1e-4)
        np.testing.assert_allclose(robot.joint_lower_limit, np.array([-2.957,-3.13,-1.9,-2.95,-2.36,-3.13,-1.9,-3.13]), atol=1e-4)
        np.testing.assert_allclose(robot.joint_upper_limit, np.array([2.957,3.13,1.9,2.95,2.36,3.13,1.9,3.13]), atol=1e-4)
        np.testing.assert_allclose(robot.joint_vel_limit, np.array([2.26,2.95,2.95,2.95,2.95,3.48,3.48,6.97]), atol=1e-4)
        np.testing.assert_allclose(robot.R_tool, np.array([[-1,0,0],[0,0,-1],[0,-1,0]]), atol=1e-4)
        np.testing.assert_allclose(robot.p_tool, np.zeros((3,)), atol=1e-4)

    def assert_right_robot(self, robot):
        np.testing.assert_allclose(robot.H, np.array([[0.,0.,0.,0.,0.,0.,0.],[1.,0.,1.,0.,-1.,0.,1.],[0.,1.,0.,-1.,0.,-1.,0.]]), atol=1e-4)
        np.testing.assert_allclose(robot.P, np.array([[0.1,0.,0.,0.,0.,0.,0.,0.],[-0.0275,-0.2255,-0.169,-0.181,-0.1936,-0.155,-0.168,0.],[0.3221,0.0577,-0.0454,-0.0085,0.0155,0.008,-0.015,0.]]), atol=1e-4)
        np.testing.assert_allclose(robot.joint_type, np.array([0.,0.,0.,0.,0.,0.,0.]), atol=1e-4)
        np.testing.assert_allclose(robot.joint_lower_limit, np.array([-3.13,-1.9,-2.95,-2.36,-3.13,-1.9,-3.13]), atol=1e-4)
        np.testing.assert_allclose(robot.joint_upper_limit, np.array([3.13,1.9,2.95,2.36,3.13,1.9,3.13]), atol=1e-4)
        np.testing.assert_allclose(robot.joint_vel_limit, np.array([2.95,2.95,2.95,2.95,3.48,3.48,6.97]), atol=1e-4)
        np.testing.assert_allclose(robot.R_tool, np.array([[1,0,0],[0,0,1],[0,-1,0]]), atol=1e-4)
        np.testing.assert_allclose(robot.p_tool, np.zeros((3,)), atol=1e-4)
    
class URDFLoaderTestSuite(unittest.TestSuite):
    def __init__(self):
        super(URDFLoaderTestSuite, self).__init__()
        self.addTest(Test_irb6640())
        self.addTest(Test_sda10f())
             
if __name__ == '__main__':
    import rosunit
    rosunit.unitrun('rpi_general_robotics_toolbox_py', \
                 'test_urdf_loader', \
                 'test_urdf_loader.URDFLoaderTestSuite')
