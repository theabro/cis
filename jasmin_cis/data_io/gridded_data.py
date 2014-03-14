import iris

from jasmin_cis.data_io.common_data import CommonData
from jasmin_cis.data_io.hyperpoint import HyperPoint
from jasmin_cis.data_io.hyperpoint_view import GriddedHyperPointView


def load_cube(*args, **kwargs):
    iris_cube = iris.load_cube(*args, **kwargs)
    return make_from_cube(iris_cube)


def make_from_cube(cube):
    gd = GriddedData(cube.data, standard_name=cube.standard_name, long_name=cube.long_name,
                     var_name=cube.var_name, units=cube.units, attributes=cube.attributes,
                     cell_methods=cube.cell_methods, dim_coords_and_dims=cube._dim_coords_and_dims,
                     aux_coords_and_dims=cube._aux_coords_and_dims, aux_factories=cube._aux_factories,
                     data_manager=cube._data_manager)
    return gd


class GriddedData(iris.cube.Cube, CommonData):
    def __init__(self, *args, **kwargs):
        super(GriddedData, self).__init__(*args, **kwargs)

    @staticmethod
    def _wrap_cube_iterator(itr):
        """Makes a generator that returns a GriddedData object from each Cube returned by an iterator.
        @param itr: iterator over Cubes
        @return: yields GriddedData objects created from Cubes
        """
        for c in itr:
            yield make_from_cube(c)

    def slices(self, *args, **kwargs):
        return self._wrap_cube_iterator(super(GriddedData, self).slices(*args, **kwargs))

    def get_coordinates_points(self):
        raise NotImplementedError

    def get_all_points(self):
        """Returns a HyperPointView of the points.
        @return: HyperPointView of all the data points
        """
        all_coords = [((c[0].points, c[1]) if c is not None else None) for c in self.find_standard_coords()]
        return GriddedHyperPointView(all_coords, self.data, cube=self)

    def get_non_masked_points(self):
        """Returns a HyperPointView of the points.
        @return: HyperPointView of all the data points
        """
        all_coords = [((c[0].points, c[1]) if c is not None else None) for c in self.find_standard_coords()]
        return GriddedHyperPointView(all_coords, self.data, non_masked_iteration=True, cube=self)

    def find_standard_coords(self):
        """Constructs a list of the standard coordinates.
        The standard coordinates are latitude, longitude, altitude, air_pressure and time; they occur in the return
        list in this order.
        @return: list of coordinates or None if coordinate not present
        """
        ret_list = []

        coords = self.coords()
        for name in HyperPoint.standard_names:
            coord_and_dim = None
            for idx, coord in enumerate(coords):
                if coord.standard_name == name:
                    coord_and_dim = (coord, idx)
                    break
            ret_list.append(coord_and_dim)

        return ret_list