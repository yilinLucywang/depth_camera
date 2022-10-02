import numpy as np
import math
import cv2

color_pic_paths = ["/Users/wangyilin/Desktop/depthPhoto/IMG_0047_c.jpg"]
class Cam(): 
    def __init__(self, angle, trans, path):
        self.angle = angle
        self.trans = trans
        self.path = path

# angle vec3 in radians((-1)* randians ori cam to cur cam)
# position in world position in vec3
# input_vec in its own camera coordinate vec4
def projection(angle, position, input_vec):
    input_vec = np.array(input_vec)
    a_x = angle[0]
    a_y = angle[1]
    a_z = angle[2]
    rot_mat_y = [[math.cos(a_y),0, -math.sin(a_y),0],
                [0, 1, 0, 0],
                [math.sin(a_y), 0, math.cos(a_y),0],
                [0, 0, 0, 1]]
    rot_mat_x = [[1,0,0,0],
                [0, math.cos(a_x), math.sin(a_x),0],
                [0, -math.sin(a_x), math.cos(a_x),0],
                [0, 0, 0, 1]]
    rot_mat_z = [[math.cos(a_z), math.sin(a_z), 0, 0],
                [-math.sin(a_z), math.cos(a_z), 0, 0],
                [0, 0, 1, 0],
                [0, 0, 0, 1]]
    rot_mat_x = np.array(rot_mat_x)
    rot_mat_y = np.array(rot_mat_y)
    rot_mat_z = np.array(rot_mat_z)
    rot_mat = np.matmul(np.matmul(rot_mat_x, rot_mat_y), rot_mat_z)
    t_x = position[0]
    t_y = position[1]
    t_z = position[2]
    trans_mat = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [t_x, t_y, t_z, 1]]
    trans_mat = np.array(trans_mat)
    inter_vec = np.matmul(rot_mat, input_vec)
    # print(inter_vec)
    # print(trans_mat)
    output_vec = np.matmul(inter_vec, trans_mat)
    # print(output_vec)
    return output_vec


#z 距离是0-1之间
#x, y 距离也应该是0-1之间
#make a dictionary that maps pt_index to positions of the pts
def map_point(pic_path, num_point, img_idx):
    idx_2_pos = {}
    path = pic_path
    img = cv2.imread(path)
    height, width = img.shape[:2]
    w_step = math.floor(width/num_point)
    h_step = math.floor(height/num_point)
    point_arr = []

    color_path = color_pic_paths[img_idx]
    color_img = cv2.imread(color_path)
    color_height, color_width = color_img.shape[:2]
    w_scale = color_width/width
    h_scale = color_height/height

    raw_edges = []
    remaining_vertices = set()
    processed_edges = []

    #construct raw edges
    v_idx_raw = 0
    horizontal_num = math.floor(width/w_step)
    vertical_num = math.floor(height/h_step)
    for x in range(horizontal_num): 
        for y in range(vertical_num): 
            cur_index = y*horizontal_num + x
            #if right in bound
            if((x + 1) < horizontal_num):
                edge_1 = [cur_index, cur_index + 1]
                raw_edges.append(edge_1)
            #if bot in bound
            if((y + 1) < vertical_num):
                edge_2 = [cur_index, (y+1)*horizontal_num + x]
                raw_edges.append(edge_2)

    v_idx = 0
    for w in range(0, width, w_step):
        for h in range(0, height, h_step): 
            curColor = img[h,w]
            dist = color_to_distance(curColor)
            #print(dist)
            if(dist <= 500):
                img_color = color_img[math.floor(h*h_scale), math.floor(w*w_scale)]
                if(img_color[0] == 255): 
                    cur_coordinate = [w/width,h/height,dist]
                    point_arr.append(cur_coordinate)
                    remaining_vertices.add(v_idx)
                    idx_2_pos[v_idx] = cur_coordinate
            v_idx = v_idx + 1
            #print(point_arr)
    for edge in raw_edges: 
        #print(edge)
        is_cur_edge = False
        t_1 = False
        t_2 = False
        for i in range(len(edge)): 
            pt = edge[i]
            if(pt in remaining_vertices): 
                if(i == 0): 
                    t_1 = True
                if(i == 1): 
                    t_2 = True
        if(t_1 and t_2): 
            processed_edges.append(edge)
    #TODO: check this
    #print(processed_edges)
    return [idx_2_pos, processed_edges]

#map point to [0,1] according to value
def color_to_distance(color): 
    #some color to distance calculation
    #print(color[0])
    colorVal = color[0]/255.0
    dist = 1/(colorVal+0.0001)
    return dist

# neighbors = []
# #先变成一张sheet 搞定
# #再把纸窝进去
# #connect sheets的边缘
# def connect_point_one_pic(processed_edges):
#     #map pt index back to position of the 


#TODO: work on this later
# #     return edgeList
# def find_neighboring_pts():
#     #TODO: 1. find the edge on the edges
#     #TODO: 1. find neighboring edges of the pics
#         #TODO: 4 edges matches 4 edges, 正着match一遍，反着match一遍，取最小
#     #TODO: 2. 

# def check_overlap(point_arr):

# def idx_2_edges(idx_2_pos, processed_edges):


#TODO: set closest object dist to 0
def main(): 
    # num_point is number of points on each dimension of the picture
    num_point = 30

    #TODO: the following is the test cam
    cam_0 = Cam([0,0,0], [0,0,0], "/Users/wangyilin/Desktop/depthPhoto/IMG_0047_depth.jpg")
    #cam_1 = Cam([0,(0.5 * math.pi),0], [0,0,0], "/Users/wangyilin/Desktop/depthPhoto/IMG_0039_depth.jpg")
    # cam_2 = Cam([0,(1 * math.pi), 0], [0,0,0], "/Users/wangyilin/Desktop/depthPhoto/test_img.jpg")
    # cam_3 = Cam([0,(1.5 * math.pi), 0], [0,0,0], "/Users/wangyilin/Desktop/depthPhoto/test_img.jpg")
    cam_arr = [cam_0]

    color_arr = ["stroke(0xffffffff);", "stroke(204, 102, 0);","stroke(204, 204, 0);","stroke(102, 204, 0);"]
    project_pt_arr = []
    f = open("/Users/wangyilin/Desktop/depthPhoto/point_file.txt", "w")
    f.close()
    f = open("/Users/wangyilin/Desktop/depthPhoto/point_file.txt", "a")
    for i in range(len(cam_arr)):
        cam = cam_arr[i]
        cur_color = color_arr[i]
        f.write(cur_color + "\n")
        idx_2_pos, processed_edges = map_point(cam.path, num_point, i)
        for idx,coordinate in idx_2_pos.items(): 
            #note the vector should end with 1
            point = [coordinate[0],coordinate[1],coordinate[2],1]
            #print(point)
            out_pt = projection(cam.angle, cam.trans, point)
            #print(out_pt)
            to_att = [out_pt[0], out_pt[1],out_pt[2]]
            #this is index to point coordinate
            idx_2_pos[idx] = to_att

            project_pt_arr.append(to_att)
            pt_1 = [200 * to_att[0], 200 * to_att[1], 200 * to_att[2]]
            f.write("point(" + str(pt_1[0]) + ", " + str(pt_1[1]) + ", " + str(pt_1[2]) + ");\n")
        for e in processed_edges: 
            #line(x1, y1, z1, x2, y2, z2)
            cur_e_pos = []
            for p_1 in e: 
                p_1_coor = idx_2_pos[p_1]
                p_1_coor = [200 * p_1_coor[0], 200 * p_1_coor[1], 200 * p_1_coor[2]]
                cur_e_pos.append(p_1_coor)
            f.write("line(" + str(cur_e_pos[0][0]) + ", " + str(cur_e_pos[0][1]) + ", " + str(cur_e_pos[0][2]) + ", " + str(cur_e_pos[1][0]) + ", " + str(cur_e_pos[1][1]) + ", " + str(cur_e_pos[1][2]) + ");\n")
    f.close() 

main()




