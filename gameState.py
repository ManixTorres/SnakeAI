import math
import copy
class GameState:
    def __init__(self,snake_head,snake_list,food_location_x,food_location_y, dis_width,dis_height,steps_since_food_eaten):
        self.snake_head = [int(snake_head[0]/10),int(snake_head[1]/10)]
        new_list = []
        for x in snake_list:
            new_list.append([int(x[0]/10),int(x[1]/10)])

        self.snake_body = new_list
        self.food_x = int(food_location_x/10)
        self.food_y = int(food_location_y/10)
        self.width = int(dis_width/10)
        self.height = int(dis_height/10)
        self.super_arr = [[0 for i in range(self.width) ] for k in range(int(self.height))]

        self.FOOD_POWER = 500
        self.CHECK_AREA = 1000 # 80% THING
        self.SQUARE = 15 # how big the area checked is
        self.LOCATION_CHECK_REWARD = 40# CHECK HOW MUCH AREA IS OCCUPIED BY SNAKE

        if steps_since_food_eaten > 500:
            self.FOOD_POWER = self.FOOD_POWER * 100

        # for i in range(0,self.height):
        #     for j in range(0,self.width):
        #         if i == 0 or j == 0 :
        #             self.super_arr[i][j] = 1
        
        
        
        #0 = free space
        #1 = wall/snake/obstacle
        #2 = food
        self.super_arr[int(self.snake_head[0])][int(self.snake_head[1])] = 1
        for x in self.snake_body:
            self.super_arr[int(x[0])][int(x[1])] = 1
        self.super_arr[int(self.food_x)][int(self.food_y)] = 2
        self.super_arr[int(self.snake_head[0])][int(self.snake_head[1])] = 1
        

    def check_legality(self,coor):
        x_coor,y_coor = coor
        x_coor = int(x_coor)
        y_coor = int(y_coor)
        # check out of bounds
        if x_coor<0:
            return False
        if y_coor<0:
            return False
        if x_coor >= self.width:
            return False
        if y_coor >= self.height:
            return False
        # Check if snake is there
        if self.super_arr[x_coor][y_coor] == 1:
            return False
        return True

    def get_legal_moves(self):
        up_x = self.snake_head[0]
        up_y = self.snake_head[1]-1

        down_x = self.snake_head[0]
        down_y = self.snake_head[1]+1

        right_x = self.snake_head[0]+1
        right_y = self.snake_head[1]

        left_x = self.snake_head[0]-1
        left_y = self.snake_head[1]
        moves = [[up_x,up_y],[down_x,down_y],[right_x,right_y],[left_x,left_y]]
        legal_moves = {}
        if self.check_legality([up_x,up_y]):
            legal_moves['up'] = [up_x,up_y]
        if self.check_legality([down_x,down_y]):
            legal_moves['down'] = [down_x,down_y]
        if self.check_legality([right_x,right_y]):
            legal_moves['right'] = [right_x,right_y]
        if self.check_legality([left_x,left_y]):
            legal_moves['left'] = [left_x,left_y]
        return legal_moves

    def get_legal_moves_spot(self,coor):
        up_x = coor[0]
        up_y = coor[1]-1

        down_x = coor[0]
        down_y = coor[1]+1

        right_x = coor[0]+1
        right_y = coor[1]

        left_x = coor[0]-1
        left_y = coor[1]
        moves = [[up_x,up_y],[down_x,down_y],[right_x,right_y],[left_x,left_y]]
        legal_moves = {}
        if self.check_legality([up_x,up_y]):
            legal_moves['up'] = [up_x,up_y]
        if self.check_legality([down_x,down_y]):
            legal_moves['down'] = [down_x,down_y]
        if self.check_legality([right_x,right_y]):
            legal_moves['right'] = [right_x,right_y]
        if self.check_legality([left_x,left_y]):
            legal_moves['left'] = [left_x,left_y]
        return legal_moves




        
    
    def print_body(self):
        print(self.snake_body)
    def get_head(self):
        return self.snake_head
    def get_body(self):
        return self.snake_body
    def get_food(self):
        return set([self.food_x,self.food_y])
    
    def check_area(self,x,y):
        total_area = self.width*self.height - len(self.snake_body) - 1
        area_available = 0
        visited_arr = copy.deepcopy(self.super_arr)
        queue = [[x,y]]
        visited_arr[x][y] = 1
        while queue:
            if area_available > total_area*0.8:
                return [True,area_available]
            curr_node = queue.pop()
            moves = self.get_legal_moves_spot(curr_node)
            for move, location in moves.items():
                if visited_arr[int(location[0])][int(location[1])] != 1:
                    visited_arr[int(location[0])][int(location[1])] = 1
                    queue.append([int(location[0]),int(location[1])])
                    area_available+=1
        return [False,area_available]
                
    
    def location_score(self,move_type,x,y):
        SQUARE = self.SQUARE
        score = 0
        REWARD = self.LOCATION_CHECK_REWARD
        x = int(x)
        y = int(y)

        if self.check_area(x,y)[0]:
            score += self.CHECK_AREA + self.check_area(x,y)[1]
        else:
            score -= self.CHECK_AREA*100

        if move_type == 'up':
            left_most = max(x-SQUARE,0)
            right_most = min(x+SQUARE, self.width)
            for i in range(left_most,right_most):
                up_most = min(y+SQUARE*2,self.height)
                for j in range(y,up_most):
                    if self.super_arr[i][j] == 1:
                        score -= REWARD
        if move_type == 'down':
            left_most = max(x-SQUARE,0)
            right_most = min(x+SQUARE, self.width)
            for i in range(left_most,right_most):
                down_most = min(y-SQUARE*2,0)
                for j in range(down_most,y):
                    if self.super_arr[i][j] == 1:
                        score -= REWARD
        if move_type == 'left':
            left_most = min(x-SQUARE*2,0)
            for i in range(left_most,x):
                down_most = max(0, y-SQUARE)
                up_most = min(self.height,y+SQUARE)
                for j in range(down_most,up_most):
                    if self.super_arr[i][j] == 1:
                        score -= REWARD
        if move_type == 'right':
            right_most = min(x+SQUARE*2,self.width)
            for i in range(x,right_most):
                down_most = max(0, y-SQUARE)
                up_most = min(self.height,y+SQUARE)
                for j in range(down_most,up_most):
                    if self.super_arr[i][j] == 1:
                        score -= REWARD

        return score


    def manhattan_distance(self,x,y):
        # distance = math.sqrt(math.pow((x-self.food_x),2) + math.pow((y-self.food_y),2))
        distance = abs(x-self.food_x) + abs(y-self.food_y)
        return distance



    def a_star(self):
        x_head,y_head = self.snake_head
        moves = self.get_legal_moves()
        best_move = None
        best_score = -float('inf')
        FACTOR = self.FOOD_POWER
        if len(self.snake_body) > 40:
            FACTOR = self.FOOD_POWER/2
        if len(self.snake_body)>70:
            FACTOR = self.FOOD_POWER/5
        # TODO ASTAR
        for move, location in moves.items():
            curr_score = self.location_score(move,location[0],location[1])
            curr_score -= self.manhattan_distance(location[0],location[1])*FACTOR
            if best_score < curr_score:
                best_move = move
                best_score = curr_score
        if best_move == None:
            best_score = -float('inf')
            for move, location in moves.items():
                curr_score = self.check_area(location[0],location[1])[1]
                if best_score < curr_score:
                    best_move = move
                    best_score = curr_score
        # print(self.snake_head)
        # print(moves)
        # print(best_move)
        return best_move

        

