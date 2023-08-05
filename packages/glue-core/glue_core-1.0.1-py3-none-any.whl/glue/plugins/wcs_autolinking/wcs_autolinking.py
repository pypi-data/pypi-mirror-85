import copy

from astropy.wcs import WCS
from astropy.wcs.utils import pixel_to_pixel
from astropy.wcs.wcsapi import SlicedLowLevelWCS, HighLevelWCSWrapper
from glue.config import autolinker, link_helper
from glue.core.link_helpers import MultiLink


__all__ = ['IncompatibleWCS', 'WCSLink', 'wcs_autolink']


class IncompatibleWCS(Exception):
    pass


def get_cids_and_functions(wcs1, wcs2, pixel_cids1, pixel_cids2):

    def forwards(*pixel_input):
        return pixel_to_pixel(wcs1, wcs2, *pixel_input)

    def backwards(*pixel_input):
        return pixel_to_pixel(wcs2, wcs1, *pixel_input)

    pixel_input = [0] * len(pixel_cids1)

    try:
        # the case with wcs linkages
        forwards(*pixel_input)
        backwards(*pixel_input)
    except Exception:
        # the case without wcs linkages
        return None, None, None, None

    return pixel_cids1, pixel_cids2, forwards, backwards


@link_helper(category='Astronomy')
class WCSLink(MultiLink):
    """
    A collection of links that link the pixel components of two datasets via
    WCS transformations.
    """

    display = 'WCS link'
    cid_independent = True

    def __init__(self, data1=None, data2=None, cids1=None, cids2=None):

        wcs1, wcs2 = data1.coords, data2.coords

        forwards = backwards = None
        if wcs1.pixel_n_dim == wcs2.pixel_n_dim and wcs1.world_n_dim == wcs2.world_n_dim:
            if (wcs1.world_axis_physical_types.count(None) == 0 and
                    wcs2.world_axis_physical_types.count(None) == 0):

                # The easiest way to check if the WCSes are compatible is to simply try and
                # see if values can be transformed for a single pixel. In future we might
                # find that this requires optimization performance-wise, but for now let's
                # not do premature optimization.

                pixel_cids1, pixel_cids2, forwards, backwards = get_cids_and_functions(wcs1, wcs2,
                                                                                       data1.pixel_component_ids[::-1],
                                                                                       data2.pixel_component_ids[::-1])

                self._physical_types_1 = wcs1.world_axis_physical_types
                self._physical_types_2 = wcs2.world_axis_physical_types

        if not forwards or not backwards:
            # A generalized APE 14-compatible way
            # Handle also the extra-spatial axes such as those of the time and wavelength dimensions

            wcs1_celestial_physical_types = wcs2_celestial_physical_types = []

            slicing_axes1 = slicing_axes2 = []

            cids1 = data1.pixel_component_ids
            cids2 = data2.pixel_component_ids

            if wcs1.has_celestial and wcs2.has_celestial:
                wcs1_celestial_physical_types = wcs1.celestial.world_axis_physical_types
                wcs2_celestial_physical_types = wcs2.celestial.world_axis_physical_types

                cids1_celestial = [cids1[wcs1.wcs.naxis - wcs1.wcs.lng - 1],
                                   cids1[wcs1.wcs.naxis - wcs1.wcs.lat - 1]]
                cids2_celestial = [cids2[wcs2.wcs.naxis - wcs2.wcs.lng - 1],
                                   cids2[wcs2.wcs.naxis - wcs2.wcs.lat - 1]]

                if wcs1.celestial.wcs.lng > wcs1.celestial.wcs.lat:
                    cids1_celestial = cids1_celestial[::-1]

                if wcs2.celestial.wcs.lng > wcs2.celestial.wcs.lat:
                    cids2_celestial = cids2_celestial[::-1]

                slicing_axes1 = [cids1_celestial[0].axis, cids1_celestial[1].axis]
                slicing_axes2 = [cids2_celestial[0].axis, cids2_celestial[1].axis]

            wcs1_sliced_physical_types = wcs2_sliced_physical_types = []

            if wcs1_celestial_physical_types is not None:
                wcs1_sliced_physical_types = wcs1_celestial_physical_types

            if wcs2_celestial_physical_types is not None:
                wcs2_sliced_physical_types = wcs2_celestial_physical_types

            for i, physical_type1 in enumerate(wcs1.world_axis_physical_types):
                for j, physical_type2 in enumerate(wcs2.world_axis_physical_types):
                    if physical_type1 == physical_type2:
                        if physical_type1 not in wcs1_sliced_physical_types:
                            slicing_axes1.append(wcs1.world_n_dim - i - 1)
                            wcs1_sliced_physical_types.append(physical_type1)
                        if physical_type2 not in wcs2_sliced_physical_types:
                            slicing_axes2.append(wcs2.world_n_dim - j - 1)
                            wcs2_sliced_physical_types.append(physical_type2)

            slicing_axes1 = sorted(slicing_axes1, key=str, reverse=True)
            slicing_axes2 = sorted(slicing_axes2, key=str, reverse=True)

            # Generate slices for the wcs slicing
            slices1 = [slice(None)] * wcs1.world_n_dim
            slices2 = [slice(None)] * wcs2.world_n_dim

            for i in range(wcs1.world_n_dim):
                if i not in slicing_axes1:
                    slices1[i] = 0

            for j in range(wcs2.world_n_dim):
                if j not in slicing_axes2:
                    slices2[j] = 0

            wcs1_sliced = SlicedLowLevelWCS(wcs1, tuple(slices1))
            wcs2_sliced = SlicedLowLevelWCS(wcs2, tuple(slices2))
            wcs1_final = HighLevelWCSWrapper(copy.copy(wcs1_sliced))
            wcs2_final = HighLevelWCSWrapper(copy.copy(wcs2_sliced))

            cids1_sliced = [cids1[x] for x in slicing_axes1]
            cids1_sliced = sorted(cids1_sliced, key=str, reverse=True)

            cids2_sliced = [cids2[x] for x in slicing_axes2]
            cids2_sliced = sorted(cids2_sliced, key=str, reverse=True)

            pixel_cids1, pixel_cids2, forwards, backwards = get_cids_and_functions(
                wcs1_final, wcs2_final, cids1_sliced, cids2_sliced)

            self._physical_types_1 = wcs1_sliced_physical_types
            self._physical_types_2 = wcs2_sliced_physical_types

        if pixel_cids1 is None:
            raise IncompatibleWCS("Can't create WCS link between {0} and {1}".format(data1.label, data2.label))

        super(WCSLink, self).__init__(pixel_cids1, pixel_cids2,
                                      forwards=forwards, backwards=backwards)

        self.data1 = data1
        self.data2 = data2

    def __gluestate__(self, context):
        state = {}
        state['data1'] = context.id(self.data1)
        state['data2'] = context.id(self.data2)
        return state

    @classmethod
    def __setgluestate__(cls, rec, context):
        self = cls(context.object(rec['data1']),
                   context.object(rec['data2']))
        return self

    @property
    def description(self):
        types1 = ''.join(['<li>' + phys_type for phys_type in self._physical_types_1])
        types2 = ''.join(['<li>' + phys_type for phys_type in self._physical_types_2])
        return ('This automatically links the coordinates of the '
                'two datasets using the World Coordinate System (WCS) '
                'coordinates defined in the files.<br><br>The physical types '
                'of the coordinates linked in the first dataset are: '
                '<ul>{0}</ul>and in the second dataset:<ul>{1}</ul>'
                .format(types1, types2))


@autolinker('Astronomy WCS')
def wcs_autolink(data_collection):

    # Find subset of datasets with WCS coordinates
    wcs_datasets = [data for data in data_collection
                    if hasattr(data, 'coords') and isinstance(data.coords, WCS)]

    # Only continue if there are at least two such datasets
    if len(wcs_datasets) < 2:
        return []

    # Find existing WCS links
    existing = set()
    for link in data_collection.external_links:
        if isinstance(link, WCSLink):
            existing.add((link.data1, link.data2))

    # Loop through all pairs of datasets, skipping pairs for which a link
    # already exists. PERF: in practice we don't actually have to link all
    # pairs, so we should try and optimize that.
    all_links = []
    for i1, data1 in enumerate(wcs_datasets):
        for data2 in wcs_datasets[i1 + 1:]:
            if (data1, data2) not in existing:
                try:
                    link = WCSLink(data1, data2)
                except IncompatibleWCS:
                    continue
                all_links.append(link)

    return all_links
