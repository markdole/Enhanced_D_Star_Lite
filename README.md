# Enhanced_D_Star_Lite
Enhancede D* Lite to avoid the Trap Obstacle and Verticle Obstacle
Enhangced D* Lite
---
基本D\*lite算法不能解决的几个障碍类型：  
 \. \. \.  
 \. \* \#  
 \# \# \#  
 当goal点在右下角时 每次`min_state`会保持在陷阱点  
 本算法解决的问题：即 判断并跳出陷阱  
 **算法的判断语句如下**
 
    def detect_Obs(self,state):
        obs = []
        for y in self.map.get_neighbers(state):
            if y.state in ['#', 'v']:
                obs.append((y.x, y.y))
        if len(obs)== 4:
            sumx = sum([i[0] - state.x for i in obs])
            sumy = sum([i[1] - state.y for i in obs])
            if [sgn(end.x - state.x), sgn(end.y - state.y)] == [sumx/3, sumy]:
                print('Type Obstacle')
                self.map.set_Virtual_obstacle([(state.x, state.y)])
                return 1
            else:
                return 0
   
   对于每一个`neighbor`检测其是否为障碍或虚拟障碍，
   当满足陷阱障碍类型 记录障碍并且将目前状态点设定为虚拟障碍
   


    def set_Virtual_obstacle(self, point_list):
        for x, y in point_list:
            if x < 0 or x >= self.row or y < 0 or y >= self.col:
                continue
            self.map[x][y].set_state("v")
继承障碍的判别方法 改变`state`为 `v` 
并且在接下来的判断函数中对h进行修改：  

        if x.state =='*' and  self.detect_Obs(x):
            for y in self.map.get_neighbers(x):
                if y.t == 'close' and y.h > k_old and y.state == '*':
                    x.parent = y
                    self.insert(y, y.h + x.cost(y))

对于新的路径点 检测到`Trap Obstacle`
每一个周围环境中的已检测点 将parent关系逆转 并重新设定逆转点的h值


