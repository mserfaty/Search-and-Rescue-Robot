class ParallelTrack:
    def __init__(self, parallel_pattern_front=False, parallel_pattern_side=False, track_width=200, area_max_value=1000):
        if parallel_pattern_front ^ parallel_pattern_side:
            self.parallel_pattern_front = parallel_pattern_front
            self.parallel_pattern_side = parallel_pattern_side
        else:
            raise ValueError("No parallel pattern specified")

        self.track_width = track_width
        self.area_max_value = area_max_value
        self.pattern = self.create_pattern()

    def create_pattern(self):
        """
        Generate coordinates for parallel tracks with specified width between tracks
        """

        # Create list of coordinates (Tuple[int, int]) between 0 and 1000 mm
        if self.parallel_pattern_front:
            pattern = [(x, y) for x in range(0, self.area_max_value + 1, self.track_width) for y in
                       (0, self.area_max_value)]
        elif self.parallel_pattern_side:
            pattern = [(y, x) for x in range(0, self.area_max_value + 1, self.track_width) for y in
                       (0, self.area_max_value)]
        else:
            raise ValueError("No pattern specified")

        # Reorder list to have the parallel pattern
        try:
            for i in range(0, len(pattern), 4):
                pattern[i + 2], pattern[i + 3] = pattern[i + 3], pattern[i + 2]
        except IndexError:
            pass

        # Put Origin to last element of list
        pattern.append(pattern[0])
        if self.parallel_pattern_side:
            pattern[0] = (0, 100)  # Go forward of 100mm before starting pattern
        else:
            pattern.pop(0)
        return pattern


class SpiralPattern:
    def __init__(self, track_width, area_max_value=1000):
        self.track_width = track_width
        self.area_max_value = area_max_value
        self.pattern = self.create_pattern()

    def create_pattern(self):
        """
        Generate coordinates for spiral pattern with specified width between patterns.
        """
        self.area_max_value = 1000

        # Create 4 lists of coordinates (Tuple[int, int]) between 0 and 1000 mm
        list1 = [(0, 0)]
        for x in range(self.track_width, int(self.area_max_value / 2) + 1, self.track_width):
            list1.append((x, list1[-1][0]))

        list2 = [(x, self.area_max_value - x) for x in range(0, int(self.area_max_value / 2) + 1, self.track_width)]
        list3 = [(x, x) for x in range(self.area_max_value, int(self.area_max_value / 2) - 1, -self.track_width)]
        list4 = [(self.area_max_value - x, x) for x in range(0, int(self.area_max_value / 2) + 1, self.track_width)]

        # Combine the 4 lists to have the spiral pattern
        pattern = []
        for k in range(len(list1)):
            pattern.append(list1[k])
            pattern.append(list2[k])
            pattern.append(list3[k])
            pattern.append(list4[k])

        # Put Origin to last element of list
        pattern.append(pattern[0])
        pattern.pop(0)
        return pattern
