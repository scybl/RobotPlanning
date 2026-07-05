#!/usr/bin/env python3

import math
import numpy as np
import rclpy

from iiwa_dynamics.iiwa14DynKDL import Iiwa14DynamicKDL
from iiwa_dynamics.iiwa14_dynamic_model import Iiwa14DynamicModel


def _rms(a):
    return math.sqrt(np.mean(np.square(a)))


def _run_case(model, reference, q, qdot):
    results = {}

    fk_model = model.forward_kinematics(q, 7)
    fk_ref = reference.forward_kinematics(q, 7)
    results['fk_rms'] = _rms(fk_model - fk_ref)

    jc_model = model.get_jacobian_centre_of_mass(q, 7)
    jc_ref = reference.get_jacobian_centre_of_mass(q, 7)
    results['jac_rms'] = _rms(jc_model - jc_ref)
    
    b_model = model.get_B(q)
    b_ref = reference.get_B(q)
    results['B_rms'] = _rms(b_model - b_ref)

    c_model = model.get_C_times_qdot(q, qdot)
    c_ref = reference.get_C_times_qdot(q, qdot)
    results['C_rms'] = _rms(c_model - c_ref)

    g_model = model.get_G(q)
    g_ref = reference.get_G(q)
    results['G_rms'] = _rms(g_model - g_ref)

    
    return results

def main():
    rclpy.init()

    model = Iiwa14DynamicModel()
    reference = Iiwa14DynamicKDL(tf_suffix='ref')

    test_cases = [
        {
            'q': [0.0, 0.1, -0.2, 0.3, -0.4, 0.5, -0.1],
            'qdot': [0.0, 0.05, 0.03, -0.02, 0.01, -0.04, 0.02],
        },
        {
            'q': [0.5, -0.6, 0.7, -0.8, 0.2, -0.1, 0.4],
            'qdot': [-0.02, 0.04, -0.01, 0.03, -0.05, 0.02, 0.01],
        }


    ]

    try:
        for idx, case in enumerate(test_cases, start=1):
            results = _run_case(model, reference, case['q'], case['qdot'])
            print(f'Case {idx}:')
            for key, value in results.items():
                print(f'  {key}: {value:.6f}')
    finally:
        model.destroy_node()
        reference.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
