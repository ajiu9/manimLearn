from manim import *

class MobiusStrip(ThreeDScene):
    """
    模拟莫比乌斯带的类。
    
    该类继承自ThreeDScene，用于创建和展示莫比乌斯带的3D动画效果。
    """
    def construct(self):
        """
        创建和展示莫比乌斯带的构造函数。
        
        该方法通过定义参数化表面和参数化函数来创建莫比乌斯带的形状，并添加一个球体来展示在莫比乌斯带上的运动。
        """
        # 设置相机的默认位置
        self.set_camera_orientation(phi=66 * DEGREES, theta=-60 * DEGREES)
        
        # 通过调整莫比乌斯带的大小间接控制场景显示范围
        scale_factor = 0.5  # 根据需要调整比例因子
        
        # 定义莫比乌斯带内外半径
        R, r = 3.2*scale_factor, 0.8*scale_factor
        
        # 定义参数化表面函数
        def mobius_surface(u, v):
            return R * np.array([np.cos(u), np.sin(u), 0]) \
                   + v * np.cos(u/2) * np.array([np.cos(u), np.sin(u), 0]) \
                   + v * np.sin(u/2) * OUT
        
        # 使用Surface创建莫比乌斯带的表面
        mobius_surface_obj = Surface(
            mobius_surface,
            resolution=(80, 16),
            color=BLUE,
            stroke_color=PINK, stroke_opacity=0.6, stroke_width=1.2*scale_factor
        )
        
        # 设置表面的透明度
        mobius_surface_obj.set_opacity(0.8)
        
        # 创建球体沿莫比乌斯带运动的高度变化
        h = 0.08*scale_factor
        
        # 定义球体的运动路径
        ball_path = lambda t: R * np.array([np.cos(t), np.sin(t), 0]) \
                           + h * np.sin(-t/2) * np.array([np.cos(t), np.sin(t), 0]) \
                           + h * np.cos(t/2) * OUT
        
        # 创建球体
        ball = Sphere(fill_color=RED, radius=0.24*scale_factor)
        
        # 初始化球体运动的时间
        self.time = 0
        
        # 定义球体的更新函数，使其沿着路径运动
        def update_ball(b, dt):
            self.time += dt/2
            b.move_to(ball_path(self.time))
        
        # 动画展示莫比乌斯带的创建
        self.play(Create(mobius_surface_obj), run_time=2)
        self.wait(1)
        
        # 注意：关于莫比乌斯带边缘的创建和消失部分，由于缺少具体实现细节，这里未提供修改代码。
        # 如果需要，应当根据当前Manim API调整或实现。
        
        # 为球体添加更新器，使其开始运动
        ball.add_updater(update_ball)
        self.add(ball)
        self.wait(20)
