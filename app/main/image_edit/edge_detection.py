from rdp import rdp
from .utils import order_points, get_polygon_area
from .visualization import draw_contours
import numpy as np
import cv2
import imutils


class PaperEdgeDetector:
    def __init__(self, image: np.ndarray):
        self.image = image
        self.original_image = image.copy()

    def get_image_edges(self):
        self._shrink_image()
        edged = edge_detection(self.image)
        longest_edge = get_longest_edge(edged)
        contour = get_contours(longest_edge)
        paper_edges = get_polygon_around_contour(contour)
        # cv2.imshow('edged', edged.astype(np.uint8))
        # cv2.imshow('conn', longest_connected_component.astype(np.uint8))
        # draw_contours(self.image, paper_edges, True, 'convex')
        simple_edges = simplify_edges(paper_edges)
        return self._get_fourgon_surrounding_paper(simple_edges).tolist()

    def _shrink_image(self):
        self.ratio = self.image.shape[0] / 500.0
        self.image = imutils.resize(self.image, height=500)

    def _get_fourgon_surrounding_paper(self, edges):
        return order_points(edges.reshape(-1, 2) * self.ratio).reshape(-1, 2).astype(np.int32)


def edge_detection(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # gray = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(gray, 30, 200)
    return edged


def get_longest_edge(edged):
    _, connected_components, stats, _ = cv2.connectedComponentsWithStats(edged,
                                                                         connectivity=8)
    label_of_longest_connected_component = stats[1:, 4].argmax() + 1
    connected_components[connected_components != label_of_longest_connected_component] = 0
    connected_components[connected_components == label_of_longest_connected_component] = 100
    return connected_components


def get_contours(connected_components):
    contour = np.array([[[b, a]] for a, b in zip(*np.where(connected_components != 0))])
    return contour


def get_polygon_around_contour(contour):
    paper_edges = cv2.convexHull(contour)
    return paper_edges


def simplify_edges(edges):
    total_area = get_polygon_area(edges.reshape(-1, 2))
    for epsilon in np.arange(0, 20, .5):
        if ((len(edges) > 4)
                and (get_polygon_area(edges.reshape(-1, 2)) > total_area * .99)
        ):
            edges = rdp(edges, epsilon=epsilon)
        else:
            break
    return edges
