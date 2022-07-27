
class RegionOfInterest:
    def BSA(self, scene):
        if scene == 'Scene_1' or scene == 'Scene_2':
            # BSA BOX COORDINATES
            x1, y1 = 1780, 200
            x2, y2 = 1880, 300

        elif scene == 'Scene_3':
            # BSA BOX COORDINATES
            x1, y1 = 1780, 155
            x2, y2 = 1860, 235

        elif scene == 'Scene_4':
            # BSA BOX COORDINATES
            x1, y1 = 1805, 340
            x2, y2 = 1885, 420

        pt1 = (x1, y1)
        pt2 = (x2, y2)

        return pt1, pt2

    def GPS(self, scene):
        if scene == 'Scene_1' or scene == 'Scene_2' or scene == 'Scene_3':
            # GPS BOX COORDINATES
            x1, y1 = 965, 500
            x2, y2 = 1375, 530

        elif scene == 'Scene_4':
            # GPS BOX COORDINATES
            x1, y1 = 985, 490
            x2, y2 = 1395, 530

        pt1 = (x1, y1)
        pt2 = (x2, y2)

        return pt1, pt2

    def Date(self, scene):
        if scene == 'Scene_1' or scene == 'Scene_3':
            # DATE BOX COORDINATES
            x1, y1 = 1295, 5
            x2, y2 = 1460, 40

        elif scene == 'Scene_2':
            # DATE BOX COORDINATES
            x1, y1 = 1295, 35
            x2, y2 = 1460, 70

        elif scene == 'Scene_4':
            # DATE BOX COORDINATES
            x1, y1 = 1235, 20
            x2, y2 = 1405, 55

        pt1 = (x1, y1)
        pt2 = (x2, y2)

        return pt1, pt2

    def Time(self, scene):
        if scene == 'Scene_1' or scene == 'Scene_3':
            # TIME BOX COORDINATES
            x1, y1 = 1470, 5
            x2, y2 = 1605, 40

        elif scene == 'Scene_2':
            # TIME BOX COORDINATES
            x1, y1 = 1470, 35
            x2, y2 = 1605, 70

        elif scene == 'Scene_4':
            # TIME BOX COORDINATES
            x1, y1 = 1410, 20
            x2, y2 = 1550, 55

        pt1 = (x1, y1)
        pt2 = (x2, y2)

        return pt1, pt2

    def DateTime(self, scene):
        if scene == 'Scene_1' or scene == 'Scene_3':
            # DATE BOX COORDINATES
            x1, y1 = 1295, 5
            x2, y2 = 1605, 40

        elif scene == 'Scene_2':
            # DATE BOX COORDINATES
            x1, y1 = 1295, 35
            x2, y2 = 1605, 70

        elif scene == 'Scene_4':
            # DATE BOX COORDINATES
            x1, y1 = 1235, 20
            x2, y2 = 1550, 55

        pt1 = (x1, y1)
        pt2 = (x2, y2)

        return pt1, pt2
