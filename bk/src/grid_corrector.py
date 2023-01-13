# -*- coding: utf-8 -*-
from grid_generator import * 
                                 
class GridCorrector(GridGenerator): 
             
    def __init__(self, rg, vfdf, res_grid_path):
        """Construtor method, initialize presets"""
        self.event = None
        self.src_axis_scale_x = rg
        self.src_axis_scale_y = vfdf
        self.msz = 8
        # set marker zoome size
        self.marker_zoom_size = 12
        # set picker
        self.pick_numb = 5
        # set numbers of points
        self.point_numb = vfdf.shape[0]
        # set path for correct grid
        self.res_grid_path = res_grid_path
        # main point collection storage 
        self.curve_points = []
        # generate points
        for i in range(self.point_numb):
            point, = plt.plot(self.src_axis_scale_x[i], self.src_axis_scale_y[i], 'bo', markersize = self.msz)
            self.curve_points.append(point)
"""
if __name__=="__main__":
    #Example usage
    tmpPath="./data/Angle(mrad)_I_DAngle_DI_sample=PIPM_10ZrO2AGM_withoutConst.prn"
    a = np.loadtxt(tmpPath)
    #print(a[:,0])
    mouse = GridCorrector(a[:,0],a[:,1])
    on_click_id = connect('button_press_event', mouse.on_click)
    on_move_id = connect('motion_notify_event', mouse.on_move)
    plt.show()
"""