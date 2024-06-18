from manim import *

config.background_color = WHITE
class Cardioid_by_Line(Scene):

    CONFIG = {
        'bg_color': WHITE,
        # 'circle_color': '#1514EA', # color blue
        # 'line_color': '#E71905', # color red
        'circle_color': RED, # color blue
        'line_color': RED, # color red
        'node_color': RED,
        'line_width': 1,
        'node_num': 9,

        'show_node_id': False,

        'circle_r': 3,
        'node_r': 0.015,

        'circle_loc': ORIGIN,
    }

    def setup(self):
        config = {**Cardioid_by_Line.CONFIG, **type(self).CONFIG}
        for key, value in config.items():
            setattr(self, key, value)

        for key, value in self.CONFIG.items():
          if hasattr(self, key):
              setattr(self, key, value)

    def construct(self):
        self.setup()
        bg_rect = Rectangle(fill_color=self.bg_color, fill_opacity=1).scale(20)
        self.add(bg_rect)
        # self.wait(0.25)

        self.anim()
        
        self.node_num=99
        self.anim()

        self.node_num=999
        self.anim()

        # self.create_all()

        # self.play(Create(self.circle), run_time=1.25)
        # self.wait(0.4)

        # for i in range(self.node_num):
        #     self.play(GrowFromCenter(self.node_group[i]), run_time=0.04)
        #     if self.show_node_id:
        #         self.play(Write(self.node_id[i]), run_time=0.06)
        # self.wait()


        zoom_in_scale = 3
        self.always_continually_update = True
        dt = 1/14.9

         # 假设self.all_objects, zoom_in_scale, dt已定义
        # center_point = self.node_group[-1].get_center()  # 缩放中心点
        # original_centers_dict = {obj: obj.get_center() for obj in self.all_objects}  # 创建对象到中心点的映射
        
        # for i in range(45):
        #     # 分别对all_objects中的每个对象进行缩放和位置调整
        #     for obj in self.all_objects:
        #         obj.scale(zoom_in_scale ** (1/45))  # 缩放对象
        #         original_center = original_centers_dict[obj]  # 使用字典获取原始中心
        #         obj.shift(original_center - center_point)  # 调整回原始相对位置
            
        #     self.wait(dt)  # 暂停dt时间


        # draw_line

        # text01 = Tex('node i', '$\\to$', 'node', color=PINK, stroke_color=WHITE).scale(1.6).to_corner(UP * 2 + LEFT * 1.6)
        # text01.set_color_by_tex_to_color_map({
        #     '$\\to$': RED_B,
        # })
        # text02 =  Tex('node 2', '$\\to$', 'node 4', color=PINK, stroke_color=WHITE).scale(1.6).to_corner(UP * 2 + LEFT * 1.6)
        # text02.set_color_by_tex_to_color_map({
        #     '$\\to$': RED_B,
        # })
        # text03 =  Tex('node 3', '$\\to$', 'node 6', color=PINK, stroke_color=WHITE).scale(1.6).to_corner(UP * 2 + LEFT * 1.6)
        # text03.set_color_by_tex_to_color_map({
        #     '$\\to$': RED_B,
        # })
        # text04 =  Tex('node 4', '$\\to$', 'node 8', color=PINK, stroke_color=WHITE).scale(1.6).to_corner(UP * 2 + LEFT * 1.6)
        # text04.set_color_by_tex_to_color_map({
        #     '$\\to$': RED_B,
        # })

        # self.play(Write(text01))
        # self.wait(0.8)
        # self.play(Create(self.line_group[0]))
        # self.wait()

        # self.play(ReplacementTransform(text01, text02))
        # self.wait(0.8)
        # self.play(Create(self.line_group[1]))
        # self.wait()

        # for i in range(15):
        #     center_point = self.node_group[-1].get_center()
            
        #     # 将所有对象平移到场景原点，以便缩放中心点变为(0,0)
        #     self.all_objects.shift(-center_point)
            
        #     # 执行缩放操作
        #     self.all_objects.scale((1/zoom_in_scale) ** (1/45))
            
        #     # 将对象移回原来的位置，完成“关于点”的缩放效果
        #     self.all_objects.shift(center_point)
            
        #     # 暂停一段时间
        #     self.wait(dt)



        # self.play(ReplacementTransform(text02, text03))
        # self.wait(0.8)
        # self.play(Create(self.line_group[2]))
        # self.wait()

        # self.play(ReplacementTransform(text03, text04))
        # self.wait(0.8)
        # self.play(Create(self.line_group[3]))
        # self.wait()
        # self.play(FadeOut(text04))

        # # for i in range(30):
        # #     self.all_objects.scale_about_point((1/zoom_in_scale) ** (1/45), self.node_group[-1].get_center())
        # #     self.wait(dt)

        # for i in range(30):
        #     center_point = self.node_group[-1].get_center()
            
        #     # 将所有对象平移到场景原点，以便缩放中心点变为(0,0)
        #     self.all_objects.shift(-center_point)
            
        #     # 执行缩放操作
        #     self.all_objects.scale((1/zoom_in_scale) ** (1/45))
            
        #     # 将对象移回原来的位置，完成“关于点”的缩放效果
        #     self.all_objects.shift(center_point)
            
        #     # 暂停一段时间
        #     self.wait(dt)

        # text_i =  Tex('node i', '$\\to$', '$node 2\\times i$', color=PINK, stroke_color=WHITE).scale(1.1).to_corner(UP * 2 + RIGHT * 1.5)
        # text_i.set_color_by_tex_to_color_map({
        #     '$\\to$': RED_B,
        # })
        # text_i02 =  Tex('2i大于n时则对n取余', color=PINK, stroke_color=WHITE)\
        #     .scale(0.9).next_to(text_i, DOWN * 0.7).align_to(text_i, LEFT)

        # self.play(Write(text_i))
        # self.wait(0.75)
        # self.play(Write(text_i02))

        # for i in range(4, self.node_num):
        #     self.play(Create(self.line_group[i]), run_time=0.25)
        #     self.wait(0.1)

        # n = 18 to 36 to 64
        # self.node_num = 18
        # old_objs = self.all_objects
        # self.create_all()
        # self.play(ReplacementTransform(old_objs, self.all_objects))
        # self.wait()
        
        # self.node_num = 36
        # old_objs = self.all_objects
        # self.create_all()
        # self.play(ReplacementTransform(old_objs, self.all_objects))
        # self.wait()
        
        # self.node_num = 64
        # old_objs = self.all_objects
        # self.create_all()
        # self.play(ReplacementTransform(old_objs, self.all_objects))
        # self.wait()

        # self.node_num = 128
        # old_objs = self.all_objects
        # self.create_all()
        # self.play(ReplacementTransform(old_objs, self.all_objects))
        # self.wait()

        # self.node_num = 256
        # old_objs = self.all_objects
        # self.create_all()
        # self.play(ReplacementTransform(old_objs, self.all_objects))
        # self.wait()

        # self.node_num = 512
        # old_objs = self.all_objects
        # self.create_all()
        # self.play(ReplacementTransform(old_objs, self.all_objects))

        # self.node_num = 1024
        # old_objs = self.all_objects
        # self.create_all()
        # self.play(ReplacementTransform(old_objs, self.all_objects))

        # self.wait(2)

    def create_all(self):

        n = self.node_num
        self.circle = Circle(radius=self.circle_r, color=self.circle_color, stroke_width=2 * self.line_width).move_to(self.circle_loc)

        self.node_group = VGroup()
        self.node_id = VGroup()
        self.line_group = VGroup()
        delta_a = TAU / n

        for i in range(n):
            vector_i = np.array([-np.sin(delta_a * (i + 1) + TAU / 2), np.cos(delta_a * (i + 1) + TAU / 2), 0]) * self.circle_r
            node_i = Circle(radius=self.node_r, color=self.node_color, fill_color=self.node_color, fill_opacity=1).move_to(self.circle.get_center() + vector_i)

            self.node_group.add(node_i)
            if self.show_node_id:
                text_i =  Tex('%d' % (i + 1), color=self.node_color).scale(0.36).move_to(self.circle.get_center() + vector_i * 1.06)
                self.node_id.add(text_i)

        for i in range(1, n+1):

            line_i = Line(self.node_group[i - 1].get_center(), self.node_group[(2 * i - 1) % n + 1 - 1].get_center(),
                          color=self.line_color, stroke_width=self.line_width)
            self.line_group.add(line_i)

        self.all_objects = VGroup(self.circle, self.node_group, self.node_id, self.line_group)

    # def anim(self):
    #     self.create_all()

    #     self.play(Create(self.circle), run_time=1.25)
    #     self.wait(0.4)

    #     for i in range(self.node_num):
    #         self.play(FadeInFromLarge(self.node_group[i]), run_time=0.06)
    #         if self.show_node_id:
    #             self.play(Write(self.node_id[i]), run_time=0.1)
    #     self.wait()

    #     for i in range(self.node_num):
    #         self.play(Create(self.line_group[i]), run_time=0.2)
    #         self.wait(0.05)
    #     self.wait()

    def anim(self):
        self.create_all()

        self.play(Create(self.circle), run_time=1.25)
        self.wait(0.4)

        screen_edge = np.array([-5, 5, 0])  # 选择一个屏幕外的位置作为初始位置
        for i in range(self.node_num):
            # 创建节点的放大版并置于屏幕外
            large_node = self.node_group[i].copy().scale(3)  # 假设放大3倍
            large_node.move_to(screen_edge)
            
            # 淡入并移至最终位置
            self.play(
                large_node.animate.move_to(self.node_group[i].get_center()).scale(1/3),
                FadeIn(large_node, shift=RIGHT),  # 调整shift参数以改变淡入方向
                run_time=0.06
            )
            self.remove(large_node)  # 可选：移除放大版节点，保持场景干净

            if self.show_node_id:
                self.play(Write(self.node_id[i]), run_time=0.1)
        self.wait()

        for i in range(self.node_num):
            self.play(Create(self.line_group[i]), run_time=0.2)
            self.wait(0.05)
        self.wait()
