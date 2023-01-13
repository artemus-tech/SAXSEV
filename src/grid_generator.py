# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt          # http://matplotlib.org
import numpy as np
import cast as ct
                                 
class GridGenerator:              
    """
    Rg - Grid Generation class
 
    """ 
    def __init__(self, q, res_grid_path):#angle, res_grid_path):
        """Construtor method, initialize presets"""
        # event definition
        self.event = None
        # evaluate scattering vector q
        #
        #q = ct.scat_vect(angle)
        #
        # set Rg limits
        RgMin = 0.5*ct.Rg_Bragg(max(q))
        RgMax = 1.5*ct.Rg_Bragg(min(q))
        # set marker size
        self.msz = 8
        # set marker zoome size
        self.marker_zoom_size = 12
        # set picker
        self.pick_numb = 5
        # set numbers of points
        #self.point_numb = 8
        self.point_numb = 200

        # generate  vector abscissa 
        self.src_axis_scale_x = np.logspace(np.log10(RgMin), np.log10(RgMax), self.point_numb)
        # generate  vector ordinat 
        self.src_axis_scale_y = np.arange(0, self.point_numb, 1)
        # set path to result grid containing file
        self.res_grid_path = res_grid_path
        # main point collection storage 
        self.curve_points = []
        # save src-generated Grid
        np.savetxt(self.res_grid_path, self.src_axis_scale_x.T)

        for i in range(self.point_numb):
            point, = plt.plot(self.src_axis_scale_x[i], self.src_axis_scale_y[i], 'bo', markersize = self.msz)
            self.curve_points.append(point)
            

    def __in_array(self,event):
        for point in self.curve_points:
            if (point.contains(event)[0] == True):
                point.remove()
                # trace, to show deleted points formed location
                plt.plot(point.get_xdata()[0], point.get_ydata()[0], 'wo', markersize = self.msz, picker = self.pick_numb)
                self.curve_points.remove(point)
        return self.curve_points

    def on_click(self, event):
        """append points"""
        for axes in event.canvas.figure.axes:
            # to prevent merge modes with adding points procedure
            if axes.get_navigate_mode() is None: 
                if event.xdata is not None and event.ydata is not None :
                    # get current axis
                    ax = plt.gca()    
                    # overlay plots.
                    #ax.hold(True) 
                    # left click branch
                    if event.button == 1:
                        point , = plt.plot(event.xdata, event.ydata, 'ro', markersize = self.msz, picker = self.pick_numb)
                        self.curve_points.append(point)
                    # right click branch
                    if event.button == 3:
                        self.curve_points = self.__in_array(event)
                    # resfresh plot
                    plt.draw()
                    # save result into file and buffer
                    res = np.unique(sorted([point.get_xdata()[0] for point in self.curve_points]))
                    np.savetxt(self.res_grid_path, res.T)

    def on_move(self,event):
        for point  in self.curve_points:
            should_be_zoomed = (point.contains(event)[0] == True)
            """onmousemove  return 30, onmouseout return 10"""
            marker_size =  2 * self.msz if should_be_zoomed else self.msz
            # zoom point
            point.set_markersize(marker_size)
        # resfresh plot
        plt.draw()
    def on_close(self,event):
        print(self.__class__.__name__)
        return self.__class__.__name__
        
        

"""
# Example usage

if __name__=="__main__":
    tmp_path="./data/Angle(mrad)_I_DAngle_DI_sample=PIPM_10ZrO2AGM_withoutConst.prn"
    np.loadtxt(tmp_path,usecols=[0,])
    mouse = GridGen(tmpPath)
    on_click_id = connect('button_press_event', mouse.on_click)
    on_move_id = connect('motion_notify_event', mouse.on_move)
    plt.show()
"""
