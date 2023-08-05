from __future__ import annotations

from typing import Tuple, Sequence, Union, TYPE_CHECKING

import numpy as np

from fibomat.shapes.arc import Arc
from fibomat.shapes.line import Line

if TYPE_CHECKING:
    from fibomat.shapes.parametric_curve import ParametricCurve

# some helpers for biarc_approximation

# for debugging
# import matplotlib as mpl
# mpl.rcParams['figure.dpi'] = 100
#
# import matplotlib.pyplot as plt
#
# def plot_circle(center, r, label=None):
#     center = np.array(center)
#     t = np.linspace(0, 2*np.pi, 1000)
#
#     plt.plot(r * np.cos(t) + center[0], r * np.sin(t) + center[1], '-', label=label)
#
# def plot_curve_segment(parametric_curve: shapes.ParametricCurve, domain):
#     points = parametric_curve.f(np.linspace(*domain, 1000))
#     plt.plot(points[:, 0], points[:, 1], '-')
#
# def plot_arc(arc: shapes.Arc, label):
#     if arc.sweep_dir:
#         t = np.linspace(arc.start_angle, arc.theta + arc.start_angle, 1000)
#     else:
#         t = np.linspace(arc.end_angle, arc.theta + arc.end_angle, 1000)
#
#     plt.plot(arc.r * np.cos(t) + arc.center[0], arc.r * np.sin(t) + arc.center[1], '-', label=label)

def _make_perp_vector(p):
    return np.array([-p[1], p[0]], dtype=p.dtype if isinstance(p, np.ndarray) else float)


class _LinearFunction:
    def __init__(self, p, p_sup):
        self.p = np.array(p)
        self.p_sup = np.array(p_sup)

    def __repr__(self):
        return 't |-> {} + t * {}'.format(self.p_sup, self.p)

    def __call__(self, u):
        return self.p_sup + u*self.p

    def parallel_to(self, other: _LinearFunction):
        return np.isclose(
            np.dot(
                self.p / np.linalg.norm(self.p),
                other.p / np.linalg.norm(other.p)
            ), 1.
        )

    def intersect_at(self, other: _LinearFunction):
        m = np.array([self.p, -other.p]).T
        b = other.p_sup - self.p_sup

        res = np.linalg.solve(m, b)

        return self.p_sup + res[0] * self.p


class _PerpBisector(_LinearFunction):
    def __init__(self, p_0, p_1):
        super().__init__(_make_perp_vector(p_1 - p_0), (p_0 + p_1) / 2)


class _Bisector(_LinearFunction):
    def __init__(self, p_0, p_1):
        p_0 = np.array(p_0)
        p_1 = np.array(p_1)
        super().__init__(p_1 - p_0, (p_0 + p_1) / 2)


def _circle_circle_intersection(circ_1, circ_2):
    c_0, r_0 = circ_1
    c_1, r_1 = circ_2

    c_0 = np.array(c_0)
    c_1 = np.array(c_1)

    d = np.linalg.norm(c_0 - c_1)

    if d > r_0 + r_1:
        raise RuntimeError
    elif d < abs(r_0 - r_1):
        raise RuntimeError
    elif np.isclose(d, 0.) and np.isclose(r_0, r_1):
        return tuple()
    else:
        a = (r_0**2 - r_1**2 + d**2) / (2 * d)

        h = np.sqrt(r_0**2 - a**2)

        c = c_0 + a * (c_1 - c_0) / d

        p_1 = np.array([
            c[0] + h * (c_1[1] - c_0[1]) / d,
            c[1] - h * (c_1[0] - c_0[0]) / d
        ])

        p_2 = np.array([
            c[0] - h * (c_1[1] - c_0[1]) / d,
            c[1] + h * (c_1[0] - c_0[0]) / d
        ])

        if np.allclose(p_1, p_2):
            return p_1,
        else:
            return p_1, p_2


def _make_biarc_segment(parametric_curve: 'ParametricCurve', biarc_domain: Tuple[float, float]):
    p_0, p_1 = parametric_curve.f(biarc_domain)

    t_0, t_1 = parametric_curve.df(biarc_domain)
    t_0 /= np.linalg.norm(t_0)
    t_1 /= np.linalg.norm(t_1)

    t_0_perp = _make_perp_vector(t_0)
    t_1_perp = _make_perp_vector(t_1)

    b_0 = _PerpBisector(p_0, p_1)
    b_1 = _PerpBisector(p_0 + t_0, p_1 + t_1)

    if b_0.parallel_to(b_1):
        return Line(p_0, p_1),
    else:
        c_j = b_0.intersect_at(b_1)

        # calc J
        arc_j_1 = Arc.from_points_center(p_0, p_1, c_j, True)
        arc_j_2 = Arc.from_points_center(p_0, p_1, c_j, False)

        if arc_j_1.length < arc_j_2.length:
            j = arc_j_1.midpoint
            sweep_dir = True
        else:
            j = arc_j_2.midpoint
            sweep_dir = False

        c_0 = _PerpBisector(p_0, j).intersect_at(_Bisector(p_0, p_0 + t_0_perp))
        arc_0 = Arc.from_points_center_tangent(p_0, j, c_0, unit_tangent_start=t_0)

        c_1 = _PerpBisector(j, p_1).intersect_at(_Bisector(p_1, p_1 + t_1_perp))
        arc_1 = Arc.from_points_center_tangent(j, p_1, c_1, unit_tangent_end=t_1)

        return arc_0, arc_1


def _make_biarc_from_spiral_segment(parametric_curve: 'ParametricCurve', biarc_domain: Tuple[float, float]):
    # u_0, u_1 = biarc_domain
    p_0, p_1 = parametric_curve.f(biarc_domain)

    t_0, t_1 = parametric_curve.df(biarc_domain)

    t_0 /= np.linalg.norm(t_0)
    t_1 /= np.linalg.norm(t_1)

    k_0, k_1 = parametric_curve.curvature(biarc_domain)

    b_0 = _PerpBisector(p_0, p_1)
    b_1 = _PerpBisector(p_0 + t_0, p_1 + t_1)

    if b_0.parallel_to(b_1):
        raise NotImplementedError
    else:
        c_j = b_0.intersect_at(b_1)
        r_j = np.linalg.norm(c_j - p_0)

        if abs(k_0) > abs(k_1):
            r_alpha = abs(1. / k_0)
            p_alpha = p_0
            t_alpha = t_0
            t_alpha_perp = np.sign(k_0) * _make_perp_vector(t_alpha)
            c_alpha = p_alpha + r_alpha * t_alpha_perp
        else:
            r_alpha = abs(1. / k_1)
            p_alpha = p_1
            t_alpha = t_1
            t_alpha_perp = np.sign(k_1) * _make_perp_vector(t_alpha)
            c_alpha = p_alpha + r_alpha * t_alpha_perp

        intersections_j_alpha = _circle_circle_intersection((c_j, r_j), (c_alpha, r_alpha))

        if len(intersections_j_alpha) == 0:
            # points lie on a circle !?
            raise NotImplementedError
        elif len(intersections_j_alpha) == 2:
            if np.allclose(intersections_j_alpha[0], p_alpha):
                j = intersections_j_alpha[1]
            elif np.allclose(intersections_j_alpha[1], p_alpha):
                j = intersections_j_alpha[0]
            else:
                raise RuntimeError
        else:
            raise RuntimeError

        if abs(k_0) > abs(k_1):
            p_beta = p_1
            t_beta = t_1
            t_beta_perp = _make_perp_vector(t_beta)
            c_beta = _Bisector(j, c_alpha).intersect_at(_Bisector(p_beta, p_beta + t_beta_perp))

            arc_alpha = Arc.from_points_center_tangent(p_alpha, j, c_alpha, unit_tangent_start=t_alpha)
            arc_beta = Arc.from_points_center_tangent(j, p_beta, c_beta, unit_tangent_end=t_beta)

        else:
            p_beta = p_0
            t_beta = t_0
            t_beta_perp = _make_perp_vector(t_beta)
            c_beta = _Bisector(j, c_alpha).intersect_at(_Bisector(p_beta, p_beta + t_beta_perp)) # plus or minus?

            arc_alpha = Arc.from_points_center_tangent(j, p_alpha, c_alpha, unit_tangent_end=t_alpha)
            arc_beta = Arc.from_points_center_tangent(p_beta, j, c_beta, unit_tangent_start=t_beta)

        if abs(k_0) > abs(k_1):
            return arc_alpha, arc_beta
        else:
            return arc_beta, arc_alpha


def _segment_is_spiral(parametric_curve: 'ParametricCurve', domain: Tuple[float, float]):
    p_0, p_1 = parametric_curve.f(domain)

    t_0, t_1 = parametric_curve.df(domain)
    t_0 /= np.linalg.norm(t_0)
    t_1 /= np.linalg.norm(t_1)

    spiral_k_0, spiral_k_1 = parametric_curve.curvature(domain)

    c_0 = _LinearFunction(_make_perp_vector(t_0), p_0).intersect_at(_PerpBisector(p_0, p_1))
    c_1 = _LinearFunction(_make_perp_vector(t_1), p_1).intersect_at(_PerpBisector(p_0, p_1))

    enclosing_k_0, enclosing_k_1 = 1./np.linalg.norm(p_0 - c_0), 1./np.linalg.norm(p_1 - c_1)

    if np.signbit(spiral_k_0) != np.signbit(spiral_k_1):
        return False

    enclosing_k_0 = np.copysign(enclosing_k_0, spiral_k_0)
    enclosing_k_1 = np.copysign(enclosing_k_1, spiral_k_1)

    if spiral_k_0 <= enclosing_k_0 and spiral_k_1 >= enclosing_k_1:
        return True
    elif spiral_k_0 >= enclosing_k_0 and spiral_k_1 <= enclosing_k_1:
        return True
    else:
        return False


def _biarc_fitting_error(
    param_curve: 'ParametricCurve',
    seg: Union[Tuple[Arc, Arc], Line],
    biarc_domain: Tuple[float, float],
    rasterized_curve_points
):
    def closest_point(points, single):
        delta = points - single
        dist = np.einsum('ij,ij->i', delta, delta)
        return np.argmin(dist)

    i_start = np.searchsorted(rasterized_curve_points[:, 0], biarc_domain[0], side='left')
    i_end = np.searchsorted(rasterized_curve_points[:, 0], biarc_domain[1], side='right')

    if len(seg) == 2:
        biarc = seg

        j_arcs = biarc[0].end
        # normal = _Bisector(j_arcs, biarc[0].center)
        # res = optimize.root(lambda u: normal(u[0]) - param_curve.f(u[1]), np.array([0., (biarc_domain[1]-biarc_domain[0])/2]))
        # thats a crude approximation to the above lines
        i_j = i_start + closest_point(rasterized_curve_points[i_start:i_end, :1], j_arcs)

        points_arc_1 = rasterized_curve_points[i_start:i_j, 1:] - biarc[0].center
        dist_arc_1 = np.abs(np.sqrt(np.einsum('ij,ij->i', points_arc_1, points_arc_1)) - biarc[0].r)

        points_arc_2 = rasterized_curve_points[i_j:i_end, 1:] - biarc[1].center
        dist_arc_2 = np.abs(np.sqrt(np.einsum('ij,ij->i', points_arc_2, points_arc_2)) - biarc[1].r)

        if len(dist_arc_1) == 0:
            return np.max(dist_arc_2)
        elif len(dist_arc_2) == 0:
            return np.max(dist_arc_1)
        else:
            return max(np.max(dist_arc_1), np.max(dist_arc_2))
    elif len(seg) == 1:
        line_: Line = seg[0]

        points = rasterized_curve_points[i_start:i_end, 1:]

        a = np.asarray(line_.start)
        n = np.asarray(line_.end - line_.start)
        n /= np.linalg.norm(n)

        dist = (a - points) - np.c_[np.dot((a - points), n) * n[0], np.dot((a - points), n) * n[1]]

        return np.max(np.abs(dist))

    else:
        raise RuntimeError


def _approximate_param_curve_greedy(param_func: 'ParametricCurve', epsilon: float):
    u_rasterized = param_func.rasterize(epsilon)
    #u_rasterized = np.linspace(*param_func.domain, int(param_func.length / epsilon) + 1, endpoint=False)

    rasterized_curve_points = np.empty(shape=(len(u_rasterized), 3), dtype=float)
    rasterized_curve_points[:, 0] = u_rasterized
    rasterized_curve_points[:, 1:] = param_func.f(u_rasterized)

    u_min, u_max = param_func.domain
    u_0, u_1 = u_min, u_min

    h = (u_max - u_min) / 10

    biarcs = []
    biarc = None

    testing = False
    is_spiral = False
    step_size_reduced = False
    end_reached = False

    while not end_reached:
        u_1 = u_0 + h

        if u_1 > u_max:
            h = u_max - u_0
            # u_1 = u_max
            end_reached = True

            interval = (u_0, u_max)
        else:
            interval = (u_0, u_1)

        if _segment_is_spiral(param_func, interval):
            if testing and not is_spiral:
                # raise RuntimeError('A non-spiral segment converted to a spiral one. This is real magic.')
                is_spiral = False
            else:
                is_spiral = True
        else:
            if testing and is_spiral:
                # extended segment is no spiral.
                # save old segment and start new one

                # print('int =', (u_0, u_1 - h_temp), 'saving', 'not a spiral')
                biarcs.extend(biarc_temp)
                u_0 = u_1 - h_temp
                # u_1 = u_0  # make sure that we are not setting u_1 = u_max.

                testing = False
                is_spiral = False
                end_reached = False
                continue
            else:
                is_spiral = False

        if is_spiral:
            biarc = _make_biarc_from_spiral_segment(param_func, interval)
        else:
            biarc = _make_biarc_segment(param_func, interval)

        # error = _dist_curve_func(curve.Curve(biarc), param_func, interval)
        error = _biarc_fitting_error(param_func, biarc, interval, rasterized_curve_points)
        print('error', error)

        if error < epsilon:
            if testing and step_size_reduced:
                biarcs.extend(biarc_temp)
                u_0 = u_1 - h_temp

                testing = False
                step_size_reduced = False
            else:
                # save current state and try again in next round with extended interval
                biarc_temp = biarc
                h_temp = h
                h *= 2

                testing = True
        else:
            end_reached = False
            if testing:
                # save state from last round
                print('int =', (u_0, u_1 - h_temp), 'saving', 'error check')
                biarcs.extend(biarc_temp)
                u_0 = u_1 - h_temp

                testing = False
            else:
                # reduce step size
                h /= 2

                step_size_reduced = True

                # T0D0: Find a good criterion for aborting
                if h < 0.1 * epsilon:
                    raise RuntimeError('Fitting does not converge.')

    if biarc:
        biarcs.extend(biarc)

    return biarcs


def approximate_parametric_curve(param_curve: 'ParametricCurve', epsilon: float) -> Sequence[Union[Arc, Line]]:
    """Approximate a ParametricCurve with an ArcSpline.

    Args:
        param_curve (ParametricCurve): curve to be approximated
        epsilon (float): maximal distance between original and approximated curve.

    Returns:
        ArcSpline

    References:
        - https://www.sciencedirect.com/science/article/pii/037704279400029Z
        - https://epub.jku.at/obvulihs/content/titleinfo/2474921
        - https://www.sciencedirect.com/science/article/abs/pii/S0010448508001681

    """
    return _approximate_param_curve_greedy(param_curve, epsilon)
