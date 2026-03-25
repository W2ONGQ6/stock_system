from PIL import Image, ImageDraw

# 为服装库存管理系统生成多尺寸 ICO 文件
sizes = [16, 32, 48, 64, 128, 256]
images = []

for size in sizes:
    # 创建带透明背景的图像
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # 计算比例
    margin = int(size * 0.1)
    
    # 背景：暖棕色圆角矩形
    radius = int(size * 0.15)
    draw.rounded_rectangle(
        [margin, margin, size - margin, size - margin],
        radius=radius,
        fill=(176, 137, 104, 255)
    )
    
    # 中心坐标
    cx, cy = size // 2, size // 2
    
    # 绘制衣架图标
    # 衣架钩子（上方小圆弧）
    hook_r = int(size * 0.08)
    hook_y = int(size * 0.25)
    draw.arc(
        [cx - hook_r, hook_y - hook_r, cx + hook_r, hook_y + hook_r],
        180, 0,
        fill='white',
        width=max(1, size // 20)
    )
    
    # 衣架三角形（主体）
    top_y = hook_y + hook_r
    bottom_y = int(size * 0.55)
    left_x = int(size * 0.2)
    right_x = int(size * 0.8)
    line_width = max(1, size // 18)
    
    # 左斜线
    draw.line([(cx, top_y), (left_x, bottom_y)], fill='white', width=line_width)
    # 右斜线
    draw.line([(cx, top_y), (right_x, bottom_y)], fill='white', width=line_width)
    # 底部横线
    draw.line([(left_x, bottom_y), (right_x, bottom_y)], fill='white', width=line_width)
    
    # 库存箱（下方）
    box_top = int(size * 0.62)
    box_bottom = int(size * 0.78)
    box_left = int(size * 0.28)
    box_right = int(size * 0.72)
    box_radius = max(1, size // 25)
    draw.rounded_rectangle(
        [box_left, box_top, box_right, box_bottom],
        radius=box_radius,
        fill='white'
    )
    
    # 库存箱内的分隔线
    line_y = int((box_top + box_bottom) / 2)
    draw.line([(box_left, line_y), (box_right, line_y)], fill=(176, 137, 104), width=1)
    
    images.append(img)

# 保存为 ICO 文件
images[0].save(
    'app.ico',
    format='ICO',
    sizes=[(s, s) for s in sizes],
    append_images=images[1:]
)
print("✓ app.ico 生成成功！包含 6 个尺寸: 16, 32, 48, 64, 128, 256")